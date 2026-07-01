---
inclusion: always
---

# API Standards — PSD2 & PCI-DSS Compliance

## Endpoint Naming
- All endpoints prefixed with `/v1/` (versioned)
- Resource names in kebab-case: `/v1/payment-initiations`, `/v1/account-information`
- Use plural nouns for collections, singular for singleton resources

## Mandatory Headers (every request)
- `X-Request-ID` — UUID, client-generated, echoed in response
- `X-Idempotency-Key` — required for all POST/PUT (state-changing) operations
- `Authorization` — Bearer token (OAuth2 / Open Banking token)
- `Content-Type` — always `application/json`

## Mandatory Response Headers
- `X-Request-ID` — echo from request
- `X-Correlation-ID` — server-generated, links all downstream calls
- `X-RateLimit-Remaining` — remaining calls in current window

## Mandatory Fields (all responses)
Every response body MUST include:
```json
{
  "transaction_id": "uuid",
  "timestamp": "ISO-8601 with timezone",
  "status": "enum value"
}
```

## Error Response Format
ALL errors must follow this structure:
```json
{
  "error": {
    "code": "PAYMENT_INSUFFICIENT_FUNDS",
    "message": "Human-readable description",
    "details": [],
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "from X-Request-ID header"
  }
}
```

Error codes: UPPER_SNAKE_CASE, prefixed by domain (PAYMENT_, ACCOUNT_, AUTH_)

## Authentication & Authorization
- OAuth2 with PKCE for TPP authentication
- Scopes: `payments:read`, `payments:write`, `accounts:read`
- Never log or store access tokens
- Validate token expiry before processing

## Data Classification
- **PAN (Primary Account Number)**: NEVER store in plaintext. Use tokenization.
- **IBAN**: May be stored, must be masked in logs (show last 4 only)
- **Customer PII**: Encrypt at rest (KMS), mask in logs
- **Transaction amounts**: Store as integer cents (avoid floating point)

## Audit Requirements
Every state-changing operation MUST:
1. Log: who, what, when, from_where (IP), request_id, correlation_id
2. Be idempotent (use X-Idempotency-Key)
3. Return the created/modified resource with its `transaction_id`
4. Emit a structured audit event to CloudWatch

## HTTP Status Codes
- 201 Created — successful payment initiation
- 200 OK — successful read
- 400 Bad Request — validation failure (include field-level errors)
- 401 Unauthorized — invalid/expired token
- 403 Forbidden — valid token, insufficient scope
- 409 Conflict — duplicate idempotency key with different payload
- 429 Too Many Requests — rate limit exceeded
- 500 Internal Server Error — never expose internal details
