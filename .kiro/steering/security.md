---
inclusion: manual
---

# Security Deep-Dive — PCI-DSS Controls

Reference this file with `#security` when performing security reviews or implementing authentication/encryption.

## PCI-DSS Requirement Mapping

### Req 3: Protect Stored Cardholder Data
- Never store PAN after authorization
- If PAN must be displayed, mask: first 6 + last 4 only
- Encryption: AES-256 via AWS KMS
- Key rotation: every 12 months minimum

### Req 4: Encrypt Transmission
- TLS 1.2+ for all external communication
- mTLS for inter-service communication
- Certificate pinning for critical downstream services

### Req 6: Develop Secure Systems
- No hardcoded credentials (use AWS Secrets Manager)
- Input validation on all user-supplied data
- Output encoding to prevent injection
- Dependency scanning in CI/CD pipeline

### Req 8: Authentication
- Strong Customer Authentication (SCA) for payment initiation
- Multi-factor authentication for admin access
- Session timeout: 5 minutes for payment flows
- Account lockout after 5 failed attempts

### Req 10: Track and Monitor Access
- All access to cardholder data must be logged
- Logs must include: user ID, timestamp, action, success/failure
- Log retention: minimum 12 months online, 3 years archive
- Tamper-evident logging (CloudWatch Logs with integrity validation)

## Secure Coding Patterns

### Input Validation
```python
from pydantic import BaseModel, Field, validator

class PaymentRequest(BaseModel):
    amount: int = Field(gt=0, le=999999999, description="Amount in cents")
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    debtor_iban: str = Field(pattern=r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$")
```

### Secrets Management
```python
# NEVER do this:
API_KEY = "sk_live_abc123"  # ❌

# ALWAYS do this:
import boto3
secrets = boto3.client("secretsmanager")
API_KEY = secrets.get_secret_value(SecretId="payment-api-key")["SecretString"]  # ✅
```

### Audit Logging
```python
import structlog

logger = structlog.get_logger()

async def initiate_payment(request: PaymentRequest, request_id: str):
    logger.info(
        "payment_initiated",
        request_id=request_id,
        amount=request.amount,
        currency=request.currency,
        # NEVER log: full IBAN, PAN, tokens
        debtor_iban_masked=mask_iban(request.debtor_iban),
    )
```
