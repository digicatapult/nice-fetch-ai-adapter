import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# happy path tests
async def test_post_query(
    app: FastAPI,
    client: AsyncClient,
    test_post_query_success_mock_202,
    test_agent_query_mock,
) -> None:
    """
    ...
    """
    payload = {
        "jsonrpc": "string",
        "method": "query",
        "params": ["string"],
        "id": "string",
    }
    response_pat = await client.post(
        app.url_path_for("test-name"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_202_ACCEPTED


# sad path tests
async def test_post_query_wrong_body(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    ...
    """
    payload = {"wrongBody": {}}
    response_pat = await client.post(
        app.url_path_for("test-name"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_post_query_failed_500(
    app: FastAPI,
    client: AsyncClient,
    test_post_query_fail_mock_500,
) -> None:
    """
    ...
    """
    payload = {
        "jsonrpc": "string",
        "method": "query",
        "params": ["string"],
        "id": "string",
    }
    response_pat = await client.post(
        app.url_path_for("test-name"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
