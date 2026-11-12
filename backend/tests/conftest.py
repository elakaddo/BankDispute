import os
import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool

from app.main import app
from app.infrastructure.database.db import Base, get_db
from app.infrastructure.database import models as _models

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not configured")


test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
def client():
    async def reset_database():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(reset_database())

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    asyncio.run(reset_database())
    asyncio.run(test_engine.dispose())


@pytest.fixture
def sample_transaction(client):
    from tests.factories.transaction_factory import transaction_payload

    response = client.post(
        "/api/v1/transactions",
        json=transaction_payload(),
    )

    assert response.status_code == 201
    return response.json()


@pytest.fixture
def sample_alert(client, sample_transaction):
    from tests.factories.alert_factory import alert_payload

    response = client.post(
        "/api/v1/alerts",
        json=alert_payload(sample_transaction["id"]),
    )

    assert response.status_code == 201
    return response.json()
