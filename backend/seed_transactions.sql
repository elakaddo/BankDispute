BEGIN;

-- 1. Suppression des transactions existantes
DELETE FROM transactions;

-- 2. Génération des 100 transactions


WITH generated AS (
    SELECT
        i,

        CASE
            WHEN i <= 80 THEN
                'tok_demo_' || LPAD((((i - 1) % 30) + 1)::TEXT, 3, '0')
            WHEN i BETWEEN 81 AND 84 THEN 'tok_demo_031'
            WHEN i BETWEEN 85 AND 88 THEN 'tok_demo_032'
            WHEN i BETWEEN 89 AND 92 THEN 'tok_demo_033'
            WHEN i BETWEEN 93 AND 96 THEN 'tok_demo_034'
            ELSE 'tok_demo_035'
        END AS card_token,

        CASE
            WHEN i <= 80 THEN
                ROUND((5 + ((i * 137) % 50000) / 100.0)::NUMERIC, 2)
            WHEN i = 81 THEN 1.00
            WHEN i = 82 THEN 2.00
            WHEN i = 83 THEN 3.00
            WHEN i = 84 THEN 249.90
            WHEN i BETWEEN 85 AND 88 THEN
                (ARRAY[189.00, 249.00, 329.00, 479.00])[i - 84]
            WHEN i BETWEEN 89 AND 92 THEN
                (ARRAY[29.90, 399.90, 799.90, 599.90])[i - 88]
            WHEN i BETWEEN 93 AND 96 THEN
                (ARRAY[400.00, 500.00, 600.00, 800.00])[i - 92]
            ELSE
                (ARRAY[19.99, 49.99, 199.99, 799.99])[i - 96]
        END AS amount,

        CASE
            WHEN i <= 80 THEN
                TIMESTAMPTZ '2026-10-01 08:00:00+00'
                + ((i * 7) % 40) * INTERVAL '1 day'
                + ((i * 37) % 600) * INTERVAL '1 minute'
            WHEN i BETWEEN 81 AND 84 THEN
                TIMESTAMPTZ '2026-11-12 09:00:00+00'
                + (i - 81) * INTERVAL '45 seconds'
            WHEN i BETWEEN 85 AND 88 THEN
                TIMESTAMPTZ '2026-11-13 22:00:00+00'
                + (i - 85) * INTERVAL '2 minutes'
            WHEN i BETWEEN 89 AND 92 THEN
                TIMESTAMPTZ '2026-11-14 01:00:00+00'
                + (i - 89) * INTERVAL '3 minutes'
            WHEN i BETWEEN 93 AND 96 THEN
                TIMESTAMPTZ '2026-11-15 02:10:00+00'
                + (i - 93) * INTERVAL '2 minutes'
            ELSE
                TIMESTAMPTZ '2026-11-15 20:00:00+00'
                + (i - 97) * INTERVAL '90 seconds'
        END AS transaction_date,

        CASE
            WHEN i <= 80 THEN
                'MER_' || LPAD(((i % 12) + 1)::TEXT, 4, '0')
            WHEN i BETWEEN 81 AND 84 THEN 'MER_ECOM_001'
            WHEN i BETWEEN 85 AND 88 THEN
                'MER_ECOM_' || LPAD((i - 84)::TEXT, 3, '0')
            WHEN i BETWEEN 89 AND 92 THEN
                'MER_INT_' || LPAD((i - 88)::TEXT, 3, '0')
            WHEN i BETWEEN 93 AND 96 THEN
                'ATM_FR_' || LPAD((i - 92)::TEXT, 3, '0')
            ELSE 'MER_ECOM_099'
        END AS merchant_id,

        CASE
            WHEN i <= 80 THEN
                (ARRAY['5411', '5812', '5999', '5732', '7011'])
                    [((i - 1) % 5) + 1]
            WHEN i BETWEEN 81 AND 84 THEN '5732'
            WHEN i BETWEEN 85 AND 88 THEN '5999'
            WHEN i BETWEEN 89 AND 92 THEN '5732'
            WHEN i BETWEEN 93 AND 96 THEN '6011'
            ELSE '5999'
        END AS merchant_category_code,

        CASE
            WHEN i <= 80 AND i % 3 = 0 THEN 'POS'::transaction_channel
            WHEN i <= 80 AND i % 3 = 1 THEN 'ECOMMERCE'::transaction_channel
            WHEN i <= 80 THEN 'ATM'::transaction_channel
            WHEN i BETWEEN 93 AND 96 THEN 'ATM'::transaction_channel
            ELSE 'ECOMMERCE'::transaction_channel
        END AS channel,

        CASE
            WHEN i BETWEEN 89 AND 92 THEN
                (ARRAY['FR', 'US', 'SG', 'US'])[i - 88]
            WHEN i BETWEEN 97 AND 100 THEN
                (ARRAY['FR', 'US', 'SG', 'US'])[i - 96]
            WHEN i <= 80 THEN
                (ARRAY['FR', 'BE', 'DE', 'ES', 'NL'])
                    [((i - 1) % 5) + 1]
            ELSE 'FR'
        END AS merchant_country,

        CASE
            WHEN i <= 80 AND i % 3 = 0 THEN
                CASE WHEN i % 2 = 0 THEN 'CHIP' ELSE 'CONTACTLESS' END
            WHEN i <= 80 AND i % 3 = 2 THEN 'CHIP'
            WHEN i BETWEEN 93 AND 96 THEN 'CHIP'
            ELSE 'ECOMMERCE'
        END AS entry_mode,

        CASE
            WHEN i <= 80 AND i % 3 IN (0, 2) THEN TRUE
            WHEN i BETWEEN 93 AND 96 THEN TRUE
            ELSE FALSE
        END AS is_card_present,

        CASE
            WHEN i <= 80 AND i % 17 = 0 THEN '05'
            WHEN i <= 80 AND i % 23 = 0 THEN '51'
            WHEN i <= 80 THEN '00'
            WHEN i BETWEEN 81 AND 84 THEN
                (ARRAY['05', '14', '05', '00'])[i - 80]
            WHEN i BETWEEN 85 AND 88 THEN
                (ARRAY['00', '00', '51', '00'])[i - 84]
            WHEN i BETWEEN 89 AND 92 THEN
                (ARRAY['00', '00', '91', '00'])[i - 88]
            WHEN i BETWEEN 93 AND 96 THEN '00'
            ELSE
                (ARRAY['05', '05', '57', '00'])[i - 96]
        END AS response_code,

        CASE
            WHEN i <= 80 THEN 'dev_' || LPAD(((i - 1) % 20 + 1)::TEXT, 3, '0')
            WHEN i BETWEEN 81 AND 84 THEN 'dev_ct_001'
            WHEN i BETWEEN 85 AND 88 THEN 'dev_vel_001'
            WHEN i BETWEEN 89 AND 92 THEN 'dev_geo_001'
            WHEN i BETWEEN 93 AND 96 THEN 'dev_atm_001'
            ELSE 'dev_3ds_001'
        END AS device_id,

        CASE
            WHEN i <= 80 AND i % 3 = 1 THEN
                CASE WHEN i % 4 = 0 THEN 'N' ELSE 'Y' END
            WHEN i BETWEEN 81 AND 84 THEN
                (ARRAY['N', 'N', 'U', 'Y'])[i - 80]
            WHEN i BETWEEN 85 AND 88 THEN
                (ARRAY['Y', 'Y', 'N', 'Y'])[i - 84]
            WHEN i BETWEEN 89 AND 92 THEN
                (ARRAY['Y', 'N', 'U', 'Y'])[i - 88]
            WHEN i BETWEEN 97 AND 100 THEN
                (ARRAY['N', 'N', 'A', 'Y'])[i - 96]
            ELSE NULL
        END AS three_ds_status

    FROM generate_series(1, 100) AS s(i)
)

INSERT INTO transactions (
    id,
    amount,
    currency,
    mti,
    stan,
    response_code,
    transaction_date,
    card_token,
    merchant_id,
    merchant_category_code,
    channel,
    entry_mode,
    merchant_country,
    is_card_present,
    terminal_id,
    card_country,
    device_id,
    three_ds_version,
    three_ds_status,
    authentication_method
)
SELECT
    gen_random_uuid(),
    amount,
    'EUR',
    '0200',
    LPAD(i::TEXT, 6, '0'),
    response_code,
    transaction_date,
    card_token,
    merchant_id,
    merchant_category_code,
    channel,
    entry_mode,
    merchant_country,
    is_card_present,
    CASE
        WHEN channel = 'ECOMMERCE'::transaction_channel THEN NULL
        ELSE 'TERM_' || merchant_id
    END,
    'FR',
    device_id,
    CASE
        WHEN channel = 'ECOMMERCE'::transaction_channel THEN '2.2.0'
        ELSE NULL
    END,
    three_ds_status,
    CASE
        WHEN channel = 'ECOMMERCE'::transaction_channel THEN '3DS'
        WHEN entry_mode = 'CONTACTLESS' THEN 'CONTACTLESS'
        ELSE 'PIN'
    END
FROM generated;

-- 3. Vérification
SELECT COUNT(*) AS total_transactions FROM transactions;

COMMIT;