"""Pydantic models for PSD2-compliant payment requests and responses."""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    """Payment lifecycle status per PSD2."""

    RECEIVED = "RCVD"
    ACCEPTED_TECHNICAL = "ACTC"
    ACCEPTED_SETTLEMENT = "ACSC"
    REJECTED = "RJCT"
    PENDING = "PDNG"
    CANCELLED = "CANC"


class DebtorAccount(BaseModel):
    """Debtor (payer) account details."""

    iban: str = Field(
        pattern=r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$",
        description="IBAN of the debtor account",
        examples=["DE89370400440532013000"],
    )
    currency: str = Field(
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code",
        examples=["EUR"],
    )


class CreditorAccount(BaseModel):
    """Creditor (payee) account details."""

    iban: str = Field(
        pattern=r"^[A-Z]{2}\d{2}[A-Z0-9]{4,30}$",
        description="IBAN of the creditor account",
        examples=["GB29NWBK60161331926819"],
    )
    name: str = Field(
        min_length=1,
        max_length=140,
        description="Name of the creditor",
    )
    currency: str = Field(
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code",
        examples=["EUR"],
    )


class Amount(BaseModel):
    """Monetary amount — always in integer cents to avoid floating point."""

    value_cents: int = Field(
        gt=0,
        le=999_999_999_99,
        description="Amount in the smallest currency unit (cents/pence)",
        examples=[10000],
    )
    currency: str = Field(
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code",
        examples=["EUR"],
    )


class PaymentInitiationRequest(BaseModel):
    """PSD2 payment initiation request."""

    debtor_account: DebtorAccount
    creditor_account: CreditorAccount
    instructed_amount: Amount
    end_to_end_identification: str = Field(
        max_length=35,
        description="Unique end-to-end transaction reference",
    )
    remittance_information: str | None = Field(
        default=None,
        max_length=140,
        description="Payment reference / description",
    )


class PaymentInitiationResponse(BaseModel):
    """PSD2 payment initiation response."""

    transaction_id: UUID = Field(description="Server-generated unique transaction ID")
    status: PaymentStatus = Field(description="Current payment status")
    timestamp: datetime = Field(description="Server timestamp (ISO-8601 with timezone)")
    debtor_account_masked: str = Field(
        description="Masked IBAN (last 4 digits visible)",
        examples=["****3000"],
    )
    creditor_account_masked: str = Field(
        description="Masked IBAN (last 4 digits visible)",
        examples=["****6819"],
    )
    instructed_amount: Amount


class ErrorDetail(BaseModel):
    """Structured error detail."""

    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Standardized error response per API standards."""

    error: dict = Field(
        description="Error object with code, message, details, timestamp, request_id",
        examples=[
            {
                "code": "PAYMENT_INSUFFICIENT_FUNDS",
                "message": "The debtor account has insufficient funds",
                "details": [],
                "timestamp": "2024-01-15T10:30:00Z",
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        ],
    )
