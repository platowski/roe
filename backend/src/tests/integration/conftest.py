import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient

from app import app


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


@pytest.fixture()
def async_client():
    from app import base_host, base_port

    base_url = "http://{base_host}:{base_port}".format(
        base_host=base_host, base_port=base_port
    )
    return AsyncClient(
        app=app,
        base_url=base_url,
    )
