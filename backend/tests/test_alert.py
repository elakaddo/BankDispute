from uuid import uuid4


def test_create_alert(client, sample_transaction):
    response = client.post(
        "/api/v1/alerts",
        json={
            "transaction_id": sample_transaction["id"],
            "alert_type": "AMOUNT_ANOMALY",
            "severity": "HIGH",
            "description": "Montant inhabituel détecté.",
            "risk_score": 87.50,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["transaction_id"] == sample_transaction["id"]
    assert data["alert_type"] == "AMOUNT_ANOMALY"
    assert data["severity"] == "HIGH"
    assert data["status"] == "NEW"


def test_create_alert_transaction_not_found(client):
    response = client.post(
        "/api/v1/alerts",
        json={
            "transaction_id": str(uuid4()),
            "alert_type": "AMOUNT_ANOMALY",
            "severity": "HIGH",
            "description": "Montant inhabituel détecté.",
        },
    )

    assert response.status_code == 404


def test_get_all_alerts_empty(client):
    response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_alerts(client, sample_alert):
    response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_alerts_multiple(client, sample_transaction):
    from tests.factories.alert_factory import alert_payload

    for severity in ["HIGH", "MEDIUM"]:
        client.post(
            "/api/v1/alerts",
            json=alert_payload(
                sample_transaction["id"],
                severity=severity,
            ),
        )

    response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_alert_by_id(client, sample_alert):
    response = client.get(f"/api/v1/alerts/{sample_alert['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == sample_alert["id"]


def test_get_alert_not_found(client):
    response = client.get(f"/api/v1/alerts/{uuid4()}")

    assert response.status_code == 404


def test_get_alert_invalid_uuid(client):
    response = client.get("/api/v1/alerts/invalid-uuid")

    assert response.status_code == 422


def test_update_alert_status(client, sample_alert):
    response = client.patch(
        f"/api/v1/alerts/{sample_alert['id']}/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_update_alert_not_found(client):
    response = client.patch(
        f"/api/v1/alerts/{uuid4()}/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 404


def test_update_alert_invalid_status(client, sample_alert):
    response = client.patch(
        f"/api/v1/alerts/{sample_alert['id']}/status",
        json={"status": "INVALID"},
    )

    assert response.status_code == 422


def test_delete_alert(client, sample_alert):
    response = client.delete(f"/api/v1/alerts/{sample_alert['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/api/v1/alerts/{sample_alert['id']}")
    assert get_response.status_code == 404


def test_delete_alert_not_found(client):
    response = client.delete(f"/api/v1/alerts/{uuid4()}")

    assert response.status_code == 404


def test_delete_alert_invalid_uuid(client):
    response = client.delete("/api/v1/alerts/invalid-uuid")

    assert response.status_code == 422
