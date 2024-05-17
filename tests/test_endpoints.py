from fastapi import FastAPI, status
from httpx import AsyncClient
from unittest.mock import MagicMock, Mock, patch


import pytest



pytestmark = pytest.mark.asyncio

veritableUrl = "http://localhost:3010"
peerUrl="http://localhost:3001/api"


async def test_post_query(
    app: FastAPI,
    client: AsyncClient,
    test_forward_query_success_mock_202,
) -> None:
    """
    ...
    """
    payload = {"message":{"content": "some test message"}}
    response_pat = await client.post(
        app.url_path_for("test-name"),
        json=payload,
    )
    print(response_pat.json())
    assert response_pat.status_code == status.HTTP_202_ACCEPTED




# def test_send_query():
#     def mockJson():
#         return {}
#     mockClient = Mock()
#     mockClient.status_code = 202
#     mockClient.json = mockJson

#     class AsyncContextManager:
#         async def __aenter__(self):
#             return self
#         async def __aexit__(self, exc_type, exc, tb):
#             pass
#         async def post(self, url):
#             return mockClient

#     patch('app.main.httpx.AsyncClient', new=MagicMock(AsyncContextManager))
#     client = TestClient(app)
#     payload = {"message":{"content": "some test message"}}
#     response = client.post("/send-query",json=payload)
#     print(type(response))
#     print(response.json())

# @pytest.fixture
# def mocked_api():
#     with respx.mock(base_url=veritableUrl) as respx_mock:
#         respx_mock.post("/drcp/request", content=[], alias="list_users")
#         ...
#         yield respx_mock

# def test_list_users(mocked_api):
#     client = TestClient(app)
#     payload = {"message":{"content": "some test message"}}
#     response = client.post("/send-query",json=payload)
#     request = mocked_api["list_users"]
#     assert request.called
#     assert response.json() == []

# return_value=httpx.Response(202)
# @respx.mock
# async def test_example():
#     my_route = respx.post(f"{veritableUrl}/drcp/request").respond(json={"some":"data"})
#     client = TestClient(app)
#     payload = {"message":{"content": "some test message"}}
#     response =await  client.post("/send-query",json=payload)
#     # response = httpx.get("https://foo.bar/")
#     print(response)
#     assert my_route.called
#     assert response.status_code == 202
# @pytest.mark.asyncio
# def test_send_query():

#     with respx.mock:
#         request = respx.post(
#             f"{veritableUrl}/drcp/request", json = {}
#             )
        
#     client = TestClient(app)
#     payload = {"message":{"content": "some test message"}}
#     response = client.post("/send-query",json=payload)
#     print(type(response))
#     print(response.json())
       
