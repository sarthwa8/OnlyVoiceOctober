"""Provider-neutral LLM access, switched by environment variables.

LLM_PROVIDER=anthropic      (default) official Anthropic SDK
LLM_PROVIDER=openai_compat  any OpenAI-compatible /chat/completions endpoint: Gemini's compatibility
                            endpoint, Groq, OpenRouter, a local Ollama server, etc.

Models: LLM_MODEL is the "smart" model (extraction, interviewer); LLM_MODEL_CHEAP plays the simulated users.
Free models are weaker, so quote verification and schema validation stay on regardless of provider.
"""

from __future__ import annotations

import json
import re

import httpx
from pydantic import BaseModel, ValidationError

from .config import get_settings

DEFAULT_ANTHROPIC = {"smart": "claude-opus-5-5", "cheap": "claude-haiku-5-5"}


def provider() -> str:
    return get_settings().llm_provider


def model_for(kind: str) -> str:
    s = get_settings()
    env = "LLM_MODEL" if kind == "smart" else "LLM_MODEL_CHEAP"
    value = (s.llm_model if kind == "smart" else s.llm_model_cheap) or s.llm_model
    if value:
        return value
    if provider() == "anthropic":
        return DEFAULT_ANTHROPIC[kind]
    raise RuntimeError(f"Set {env} (and LLM_BASE_URL / LLM_API_KEY) for LLM_PROVIDER={provider()}")


def _chat_openai_compat(system: str, messages: list[dict], model: str, max_tokens: int, json_mode: bool = False) -> str:
    s = get_settings()
    if not s.llm_base_url:
        raise RuntimeError(f"Set LLM_BASE_URL for LLM_PROVIDER={provider()}")
    base = s.llm_base_url
    body: dict = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "system", "content": system}, *messages]}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    resp = httpx.post(
        f"{base}/chat/completions",
        json=body,
        headers={"Authorization": f"Bearer {s.llm_api_key}"},
        timeout=120.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"] or ""


def complete(system: str, messages: list[dict], kind: str = "smart", max_tokens: int = 600, effort: str | None = None) -> str:
    """One chat completion. `messages` use plain string content. `effort` applies to Anthropic only."""
    model = model_for(kind)
    if provider() == "anthropic":
        import anthropic

        kwargs = {"output_config": {"effort": effort}} if effort else {}
        resp = anthropic.Anthropic().messages.create(
            model=model, max_tokens=max_tokens, system=system, messages=messages, **kwargs
        )
        return "".join(b.text for b in resp.content if b.type == "text")
    return _chat_openai_compat(system, messages, model, max_tokens)


_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.I)


def _json_text(raw: str) -> str:
    text = _FENCE.sub("", raw.strip())
    start, end = text.find("{"), text.rfind("}")
    return text[start : end + 1] if start != -1 and end > start else text


def extract_structured(system: str, user: str, schema: type[BaseModel], client=None, max_tokens: int = 8000) -> BaseModel:
    """Return a validated `schema` instance. Anthropic uses native structured outputs; others use JSON + retry."""
    model = model_for("smart")
    if provider() == "anthropic":
        if client is None:
            import anthropic

            client = anthropic.Anthropic()
        resp = client.messages.parse(
            model=model,
            max_tokens=16000,
            output_config={"effort": "medium"},
            system=system,
            messages=[{"role": "user", "content": user}],
            output_format=schema,
        )
        if resp.stop_reason == "refusal" or resp.parsed_output is None:
            raise RuntimeError(f"Extraction failed: stop_reason={resp.stop_reason}")
        return resp.parsed_output

    instructions = (
        f"{system}\n\nReply with ONLY one JSON object (no prose, no code fences) that matches this JSON Schema:\n"
        f"{json.dumps(schema.model_json_schema())}"
    )
    messages = [{"role": "user", "content": user}]
    last_error = ""
    for _ in range(2):
        raw = _chat_openai_compat(instructions, messages, model, max_tokens, json_mode=True)
        try:
            return schema.model_validate_json(_json_text(raw))
        except (ValidationError, ValueError) as exc:
            last_error = str(exc)[:600]
            messages = [
                {"role": "user", "content": user},
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"That did not validate: {last_error}\nReturn the corrected JSON object only."},
            ]
    raise RuntimeError(f"Model did not return valid JSON for {schema.__name__}: {last_error}")
