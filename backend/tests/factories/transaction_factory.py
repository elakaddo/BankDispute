def transaction_payload(**overrides):
    payload = {
        "amount": {"amount": "150.00", "currency": "EUR"},
        "mti": "0200",
        "stan": "123456",
        "response_code": "00",
        "transaction_date": "2026-11-12T10:30:00Z",
        "card_token": "tok_test_001",
        "merchant_id": "MERCHANT_001",
        "terminal_id": "TERM_001",
        "merchant_category_code": "5411",
        "channel": "POS",
        "entry_mode": "CHIP",
        "merchant_country": "FR",
        "card_country": "FR",
        "device_id": "DEVICE_001",
        "is_card_present": True,
        "three_ds_version": None,
        "three_ds_status": None,
        "authentication_method": None,
    }

    payload.update(overrides)
    return payload
