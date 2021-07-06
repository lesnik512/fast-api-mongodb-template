import asyncio

import pytest
from starlette.testclient import TestClient

from app.db import drop_database
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def clean_db():
    await drop_database()


@pytest.fixture(scope="session")
def event_loop():
    """custom event loop, fix for motor's run_in_executor"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
