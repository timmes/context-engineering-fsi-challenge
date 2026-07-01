---
inclusion: always
---

# Technology Stack

## Language & Framework
- Python 3.11+
- FastAPI (async, high-performance)
- Pydantic v2 for data validation
- Mangum for AWS Lambda adapter

## Infrastructure
- AWS Lambda (compute)
- API Gateway (HTTP routing)
- DynamoDB (transaction storage)
- AWS KMS (encryption key management)
- CloudWatch (observability)

## Development Tools
- `uv` for package management
- `pytest` + `pytest-asyncio` for testing
- `ruff` for linting
- `mypy` for type checking

## Key Libraries
- `python-jose` for JWT handling
- `cryptography` for PCI-DSS compliant encryption
- `structlog` for structured logging
- `httpx` for async HTTP client

## Conventions
- Use `async def` for all route handlers
- Type-annotate all function signatures
- Use dependency injection via FastAPI's `Depends()`
- Environment config via pydantic-settings `BaseSettings`
