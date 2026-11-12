from tests.factories.transaction_factory import transaction_payload

# =========================
# GET ALL
# =========================


def test_get_all_transactions_empty(client):
    response = client.get("/api/v1/transactions")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_transactions(client, sample_transaction):
    response = client.get("/api/v1/transactions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == sample_transaction["id"]


def test_get_all_transactions_multiple(client):
    client.post("/api/v1/transactions", json=transaction_payload())
    client.post(
        "/api/v1/transactions",
        json=transaction_payload(stan="654321", response_code="05"),
    )

    response = client.get("/api/v1/transactions")

    assert response.status_code == 200
    assert len(response.json()) == 2


# =========================
# CREATE
# =========================


def test_create_transaction(client):
    payload = transaction_payload()

    response = client.post("/api/v1/transactions", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["amount"] == "150.00"
    assert data["currency"] == "EUR"
    assert data["mti"] == "0200"
    assert data["stan"] == "123456"
    assert data["response_code"] == "00"
    assert data["channel"] == "POS"
    assert data["merchant_category_code"] == "5411"
    assert data["is_card_present"] is True
    assert data["card_token"] == "tok_test_001"
    assert data["created_at"] is not None


def test_create_transaction_invalid_mti(client):
    payload = transaction_payload(mti="200")

    response = client.post("/api/v1/transactions", json=payload)

    assert response.status_code == 422


def test_create_transaction_invalid_channel(client):
    payload = transaction_payload(channel="INVALID")

    response = client.post("/api/v1/transactions", json=payload)

    assert response.status_code == 422


# =========================
# GET BY ID
# =========================


def test_get_transaction_by_id(client, sample_transaction):
    transaction_id = sample_transaction["id"]

    response = client.get(f"/api/v1/transactions/{transaction_id}")

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id
    assert response.json()["currency"] == "EUR"


def test_get_transaction_not_found(client):
    response = client.get("/api/v1/transactions/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_get_transaction_invalid_uuid(client):
    response = client.get("/api/v1/transactions/invalid-uuid")

    assert response.status_code == 422


# =========================
# DELETE
# =========================


def test_delete_transaction(client, sample_transaction):
    transaction_id = sample_transaction["id"]

    response = client.delete(f"/api/v1/transactions/{transaction_id}")

    assert response.status_code == 204
    assert response.content == b""

    # Vérifier que la transaction a réellement disparu
    get_response = client.get(f"/api/v1/transactions/{transaction_id}")

    assert get_response.status_code == 404


def test_delete_transaction_not_found(client):
    response = client.delete(
        "/api/v1/transactions/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


def test_delete_transaction_invalid_uuid(client):
    response = client.delete("/api/v1/transactions/invalid-uuid")

    assert response.status_code == 422
