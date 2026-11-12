def alert_payload(transaction_id, **overrides):
    payload = {
        "transaction_id": str(transaction_id),
        "alert_type": "AMOUNT_ANOMALY",
        "severity": "HIGH",
        "description": "Montant inhabituel détecté.",
        "risk_score": None,
    }

    payload.update(overrides)
    return payload
