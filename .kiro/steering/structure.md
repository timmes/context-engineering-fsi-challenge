---
inclusion: always
---

# Project Structure

```
src/
├── main.py              App entry point, FastAPI app creation
├── models.py            Pydantic models (request/response schemas)
├── config.py            Settings via pydantic-settings
├── routes/
│   └── payments.py      Payment initiation endpoints
├── middleware/
│   └── audit.py         Request/response audit logging
├── services/
│   └── payment_service.py  Business logic layer
└── utils/
    ├── encryption.py    KMS-backed encryption utilities
    └── errors.py        Standardized error responses

tests/
├── conftest.py          Shared fixtures
├── test_payments.py     Payment endpoint tests
└── test_models.py       Pydantic model validation tests
```

## Import Conventions
- Absolute imports only: `from src.models import PaymentRequest`
- Group imports: stdlib → third-party → local (separated by blank lines)
- Never use wildcard imports (`from x import *`)

## File Naming
- Snake_case for all Python files
- One router per domain (payments, accounts, consents)
- Tests mirror source structure: `src/routes/payments.py` → `tests/test_payments.py`
