# Real Bolna payloads go here

After the first real test call, save the **completed** webhook body as `bolna_completed.json` (redact phone numbers).
Then: (1) point a test at it, (2) check where `invite_token` / `channel` appear (`context_details` or `context_details.recipient_data`),
(3) adjust `webhook.py` if the transcript shape differs from what `test_core.py` assumes.
The fake `PAYLOAD` in `test_core.py` is synthetic: it proves the parser, not Bolna's real format.
