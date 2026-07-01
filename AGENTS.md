# Open Banking API — Context for AI Coding Agents

This is a PSD2-compliant payment initiation API built with Python/FastAPI.

## Key Conventions
- All monetary amounts are in integer cents (never use float)
- IBANs must be validated with regex and masked in logs (show last 4 only)
- Every state-changing endpoint requires X-Request-ID and X-Idempotency-Key headers
- Error responses follow the standardized format in .kiro/steering/api-standards.md
- All route handlers must be async
- Type-annotate every function signature

## Commands
- Run tests: `pytest`
- Lint: `ruff check .`
- Type check: `mypy src/`
- Start dev server: `uvicorn src.main:app --reload --port 8000`

## Never Do
- Store PAN (Primary Account Number) in plaintext
- Log access tokens or full IBANs
- Use floating point for money
- Return internal stack traces in error responses
- Skip idempotency handling on POST endpoints
