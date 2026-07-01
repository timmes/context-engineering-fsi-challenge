"""Tests for payment initiation endpoints."""

import uuid

import pytest


@pytest.mark.asyncio
async def test_initiate_payment_success(client):
    """Test successful payment initiation returns 201 with correct fields."""
    payload = {
        "debtor_account": {
            "iban": "DE89370400440532013000",
            "currency": "EUR",
        },
        "creditor_account": {
            "iban": "GB29NWBK60161331926819",
            "name": "Test Creditor",
            "currency": "EUR",
        },
        "instructed_amount": {
            "value_cents": 10000,
            "currency": "EUR",
        },
        "end_to_end_identification": "E2E-REF-001",
        "remittance_information": "Invoice 12345",
    }

    response = await client.post(
        "/v1/payment-initiations",
        json=payload,
        headers={
            "X-Request-ID": str(uuid.uuid4()),
            "X-Idempotency-Key": str(uuid.uuid4()),
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 201
    data = response.json()

    # Mandatory response fields per API standards
    assert "transaction_id" in data
    assert "timestamp" in data
    assert "status" in data
    assert data["status"] == "RCVD"

    # IBANs must be masked
    assert data["debtor_account_masked"] == "****3000"
    assert data["creditor_account_masked"] == "****6819"

    # Response headers
    assert "X-Request-ID" in response.headers
    assert "X-Correlation-ID" in response.headers


@pytest.mark.asyncio
async def test_initiate_payment_missing_headers(client):
    """Test that missing mandatory headers return 422."""
    payload = {
        "debtor_account": {"iban": "DE89370400440532013000", "currency": "EUR"},
        "creditor_account": {"iban": "GB29NWBK60161331926819", "name": "Test", "currency": "EUR"},
        "instructed_amount": {"value_cents": 5000, "currency": "EUR"},
        "end_to_end_identification": "E2E-REF-002",
    }

    # Missing X-Request-ID and X-Idempotency-Key
    response = await client.post(
        "/v1/payment-initiations",
        json=payload,
        headers={"Authorization": "Bearer test-token"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_initiate_payment_invalid_iban(client):
    """Test that invalid IBAN format is rejected."""
    payload = {
        "debtor_account": {"iban": "INVALID", "currency": "EUR"},
        "creditor_account": {"iban": "GB29NWBK60161331926819", "name": "Test", "currency": "EUR"},
        "instructed_amount": {"value_cents": 5000, "currency": "EUR"},
        "end_to_end_identification": "E2E-REF-003",
    }

    response = await client.post(
        "/v1/payment-initiations",
        json=payload,
        headers={
            "X-Request-ID": str(uuid.uuid4()),
            "X-Idempotency-Key": str(uuid.uuid4()),
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_initiate_payment_negative_amount(client):
    """Test that negative/zero amount is rejected."""
    payload = {
        "debtor_account": {"iban": "DE89370400440532013000", "currency": "EUR"},
        "creditor_account": {"iban": "GB29NWBK60161331926819", "name": "Test", "currency": "EUR"},
        "instructed_amount": {"value_cents": -100, "currency": "EUR"},
        "end_to_end_identification": "E2E-REF-004",
    }

    response = await client.post(
        "/v1/payment-initiations",
        json=payload,
        headers={
            "X-Request-ID": str(uuid.uuid4()),
            "X-Idempotency-Key": str(uuid.uuid4()),
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_payment_status_not_found(client):
    """Test querying non-existent payment returns 404."""
    fake_id = str(uuid.uuid4())

    response = await client.get(
        f"/v1/payment-initiations/{fake_id}",
        headers={
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": "Bearer test-token",
        },
    )

    assert response.status_code == 404
