# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import AsyncMock, patch
# from extra.main import app, get_http_client
# import httpx
# veritableUrl = "http://localhost:3010"
# client = TestClient(app)

# @pytest.fixture
# def mock_http_client():
#     mock = AsyncMock(httpx.AsyncClient)
#     with patch('app.main.get_http_client', return_value=mock):
#         yield mock

# def test_send_query(mock_http_client):
#     # Mock the post method to return a response with status code 202
#     mock_http_client.post.return_value = AsyncMock(status_code=202, json=lambda: {"success": True})

#     # Make a POST request to the /send-query endpoint
#     response = client.post("/send-query", json={"message": {"content": "some test message"}})

#     # Assert the response status code and JSON content
#     assert response.status_code == 202
#     assert response.json() == {"success": True}

#     # Assert that the mock post method was called with the correct arguments
#     mock_http_client.post.assert_called_once_with(
#         f"{veritableUrl}/drcp/request",
#         json={"message": {"content": "some test message"}}
#     )
