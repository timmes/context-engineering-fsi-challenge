"""Payment initiation endpoints — PSD2 compliant."""

import uuid
from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Header, HTTPException, status

from src.models import (
    ErrorResponse,
    PaymentInitiationRequest,
    PaymentInitiationResponse,
    PaymentStatus,
)

logger = structlog.get_logger()
router = APIRouter(tags=["payments"])


def _mask_iban(iban: str) -> str:
    """Mask IBAN showing only last 4 characters."""
    return f"****{iban[-4:]}"


@router.post(
    "/payment-initiations",
    response_model=PaymentInitiationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def initiate_payment(
    request: PaymentInitiationRequest,
    x_request_id: str = Header(..., alias="X-Request-ID"),
    x_idempotency_key: str = Header(..., alias="X-Idempotency-Key"),
    authorization: str = Header(...),
) -> PaymentInitiationResponse:
    """Initiate a PSD2-compliant payment.

    Requires:
    - Valid OAuth2 token with `payments:write` scope
    - X-Request-ID (UUID, client-generated)
    - X-Idempotency-Key (for duplicate detection)
    """
    transaction_id = uuid.uuid4()
    timestamp = datetime.now(tz=timezone.utc)

    # Audit log — mandatory for all state-changing operations
    logger.info(
        "payment_initiated",
        transaction_id=str(transaction_id),
        request_id=x_request_id,
        idempotency_key=x_idempotency_key,
        amount_cents=request.instructed_amount.value_cents,
        currency=request.instructed_amount.currency,
        debtor_iban_masked=_mask_iban(request.debtor_account.iban),
        creditor_iban_masked=_mask_iban(request.creditor_account.iban),
        timestamp=timestamp.isoformat(),
    )

    # TODO: Implement actual payment processing
    # - Validate OAuth2 token and scopes
    # - Check idempotency key for duplicates
    # - Call core banking system
    # - Store transaction record (DynamoDB)

    return PaymentInitiationResponse(
        transaction_id=transaction_id,
        status=PaymentStatus.RECEIVED,
        timestamp=timestamp,
        debtor_account_masked=_mask_iban(request.debtor_account.iban),
        creditor_account_masked=_mask_iban(request.creditor_account.iban),
        instructed_amount=request.instructed_amount,
    )


@router.get(
    "/payment-initiations/{transaction_id}",
    response_model=PaymentInitiationResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def get_payment_status(
    transaction_id: uuid.UUID,
    x_request_id: str = Header(..., alias="X-Request-ID"),
    authorization: str = Header(...),
) -> PaymentInitiationResponse:
    """Retrieve the status of a payment initiation.

    Requires valid OAuth2 token with `payments:read` scope.
    """
    logger.info(
        "payment_status_queried",
        transaction_id=str(transaction_id),
        request_id=x_request_id,
    )

    # TODO: Implement actual lookup from DynamoDB
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": {
                "code": "PAYMENT_NOT_FOUND",
                "message": f"Payment with transaction_id {transaction_id} not found",
                "details": [],
                "timestamp": datetime.now(tz=timezone.utc).isoformat(),
                "request_id": x_request_id,
            }
        },
    )
