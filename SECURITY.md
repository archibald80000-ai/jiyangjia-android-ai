# Security Policy

## Sensitive data

Do not open public issues containing credentials, personal information, customer audio, private network details or proprietary documents. Revoke any exposed credential immediately and purge it from Git history.

## Repository rules

- `.env.local`, `.env.*.local`, keys, certificates, recordings, logs, databases and model weights are ignored.
- Android clients receive only scoped short-lived tokens.
- Server-to-provider credentials remain server-side.
- Public test knowledge contains only approved, non-sensitive mock or public-facing content.

## Reporting

Use a private channel with the repository owner for security disclosures. Do not publish proof-of-concept credentials or private customer data.
