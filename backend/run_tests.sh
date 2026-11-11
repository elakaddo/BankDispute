
#!/bin/bash
set -e
uv sync


if [ ! -f .env.test ]; then
    echo "Erreur : .env.test introuvable"
    exit 1
fi

set -a
source .env.test
set +a

: "${TEST_DATABASE_URL:?TEST_DATABASE_URL manquante dans .env.test}"


if [ -z "$1" ]; then
    uv run pytest tests/ -v
else
    uv run pytest "tests/test_$1.py" -v
fi
