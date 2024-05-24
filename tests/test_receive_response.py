import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# happy path tests


async def test_receive_response(
    app: FastAPI,
    client: AsyncClient,
    test_receive_response_success_mock_200,
) -> None:
    """
    ...
    """
    payload = {"jsonrpc": "string", "result": "string", "id": "string"}
    response_pat = await client.post(
        app.url_path_for("receive-response"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_200_OK


# Sad path tests


async def test_receive_response_fail_500(
    app: FastAPI,
    client: AsyncClient,
    test_receive_response_fail_mock_500,
) -> None:
    """
    ...
    """
    payload = {"jsonrpc": "string", "result": "string", "id": "string"}
    response_pat = await client.post(
        app.url_path_for("receive-response"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
