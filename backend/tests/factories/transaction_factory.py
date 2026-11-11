def transaction_payload(**overrides):
    payload = {
        "amount": {"amount": "150.00", "currency": "EUR"},
        "mti": "0200",
        "stan": "123456",
        "response_code": "00",
    }

    payload.update(overrides)
    return payload
