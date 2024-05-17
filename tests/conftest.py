import pytest
from fastapi import FastAPI
from asgi_lifespan import LifespanManager
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def app() -> FastAPI:
    """
    Sets up an application instance for testing
    """
    from app.main import app  # local import for testing purpose

    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    """
    Sets up an async test runner client for testing
    """
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
def test_forward_query_success_mock_202(mocker) -> None:
    """
    Test return data for the 202 response from veritable when forwarding a query.
    """
    mocker.patch(
        "routes.posts.postToVeritable",
        return_value=[
            "202",
            {},
        ],
    )