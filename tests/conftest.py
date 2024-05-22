import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient


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
def test_post_query_success_mock_202(mocker) -> None:
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


@pytest.fixture
def test_agent_query_mock(mocker) -> None:
    """
    Test return data for the 202 response fromquery agent.
    """
    mocker.patch(
        "routes.posts.agent_query",
        return_value=[
            {"Successful query response from the Sample Agent"},
        ],
    )


@pytest.fixture
def test_receive_response_success_mock_200(mocker) -> None:
    """
    Test return data for the 200 receive response forwarding to veritable.
    """
    mocker.patch(
        "routes.posts.postResponseToVeritable",
        return_value=[
            "200",
            {},
        ],
    )


@pytest.fixture
def test_receive_response_fail_mock_500(mocker) -> None:
    """
    Test return data for the 500 receive response forwarding to veritable.
    """
    mocker.patch(
        "routes.posts.postResponseToVeritable",
        return_value=[
            "500",
            {},
        ],
    )


@pytest.fixture
def test_drcp_event_handler_response_success_mock_200(mocker) -> None:
    """
    Test return data for forwarding data from the "/webhooks/drpc" endpoint to /receive-response endpoint in peerAPI.
    """
    mocker.patch(
        "routes.posts.peerReceivesResponse",
        return_value=[
            "200",
            {},
        ],
    )


@pytest.fixture
def test_drcp_event_handler_query_success_mock_200(mocker) -> None:
    """
    Test return data for forwarding data from the "/webhooks/drpc" endpoint to /receive-query endpoint in peerAPI.
    """
    mocker.patch(
        "routes.posts.peerReceivesQuery",
        return_value=[
            "200",
            {},
        ],
    )


@pytest.fixture
def test_drcp_event_handler_query_fail_mock_500(mocker) -> None:
    """
    Test failed return data for forwarding data from the "/webhooks/drpc" endpoint to /receive-query endpoint in peerAPI.
    """
    mocker.patch(
        "routes.posts.peerReceivesQuery",
        return_value=[
            "500",
            {},
        ],
    )


@pytest.fixture
def test_post_query_fail_mock_500(mocker) -> None:
    """
    Test return data for 500 response from veritable when forwarding a query.
    """
    mocker.patch(
        "routes.posts.postToVeritable",
        return_value=[
            "500",
            {},
        ],
    )
