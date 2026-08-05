# Integration agent rules

- Respect `config/upstream-lock.json`.
- Prefer clients and adapters over editing upstream.
- Record provider API version/source and do not invent parameters.
- Mock implementations are labelled and selectable by configuration.
- Chargeable API tests use explicit small inputs and finite retries.
