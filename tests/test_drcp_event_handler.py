import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


# happy path tests
async def test_drcp_event_handler_response(
    app: FastAPI,
    client: AsyncClient,
    test_drcp_event_handler_response_success_mock_200,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
  "response": {
    "jsonrpc": "string",
    "result": "string",
    "error": {
      "code": -32601,
      "message": "string",
      "data": "string"
    },
    "id": "string"
  },
  "connectionId": "string",
  "role": "client",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_200_OK

async def test_drcp_event_handler_query(
    app: FastAPI,
    client: AsyncClient,
    test_drcp_event_handler_query_success_mock_200,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
    "request": {
    "jsonrpc": "string",
    "method": "string",
    "params": [
      "string"
    ],
    "id": "string"
  },
  "connectionId": "string",
  "role": "server",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_200_OK

  # Sad path tests 
async def test_receive_response_422(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    ...
    """
    payload = {"some":"wrong body"}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_receive_response_500(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
  "request": {
    "jsonrpc": "string",
    "method": "string",
    "params": [
      "string"
    ],
    "id": "string"
  },
  "response": {
    "jsonrpc": "string",
    "result": "string",
    "error": {
      "code": -32601,
      "message": "string",
      "data": "string"
    },
    "id": "string"
  },
  "connectionId": "string",
  "role": "client",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
 
async def test_drcp_event_handler_query_wrong_role(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
    "request": {
    "jsonrpc": "string",
    "method": "string",
    "params": [
      "string"
    ],
    "id": "string"
  },
  "connectionId": "string",
  "role": "client",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

async def test_drcp_event_handler_response_wrong_role(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
  "response": {
    "jsonrpc": "string",
    "result": "string",
    "error": {
      "code": -32601,
      "message": "string",
      "data": "string"
    },
    "id": "string"
  },
  "connectionId": "string",
  "role": "server",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

async def test_drcp_event_handler_query_fail_500(
    app: FastAPI,
    client: AsyncClient,
    test_drcp_event_handler_query_fail_mock_500,
) -> None:
    """
    ...
    """
    payload = {
  "createdAt": "2024-05-20T08:51:21.630Z",
    "request": {
    "jsonrpc": "string",
    "method": "string",
    "params": [
      "string"
    ],
    "id": "string"
  },
  "connectionId": "string",
  "role": "server",
  "state": "request-sent",
  "threadId": "string",
  "id": "string"
}
    response_pat = await client.post(
        app.url_path_for("webhooks-drpc"),
        json=payload,
    )
    assert response_pat.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR