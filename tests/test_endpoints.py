import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
import requests_mock
import json

veritableUrl = "http://localhost:3010"
peerUrl="http://localhost:3001/api"

class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data 


@pytest.fixture
def client():
    return TestClient(app)






# happy path 
def test_send_query(client,mocker):
    payload = {"message":{"content": "some test message"}}
    payload_dict = dict(payload)
    mock_response_data = {"result": "mocked_response"}
    mocker.patch('app.main.requests.post', return_value=MockResponse(200, mock_response_data),)
    response = client.post("/send-query", json=payload_dict)
    assert response.status_code == 200
    assert response.json()['json_data'] == mock_response_data

def test_drpc_event_handler(client,mocker):
    payload = {
  "createdAt": "2024-05-15T08:19:38.804Z",
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
    payload_dict = dict(payload)
    mock_response_data = {"result": "mocked_response 2"}
    mocker.patch('app.main.requests.post', return_value=MockResponse(200, mock_response_data))
    response = client.post("/webhooks/drpc", json=payload_dict)
    assert response.status_code == 200
    assert response.json()['json_data'] == mock_response_data

def test_receive_response(client,mocker):
    payload = {"message":{"jsonrpc": "2.0", "result": -19, "id": 2}}
    payload_dict = dict(payload)
    mock_response_data = {"result": "mocked_response 3"}
    mocker.patch('app.main.requests.post', return_value=MockResponse(200, mock_response_data))
    response = client.post("/receive-response", json=payload_dict)
    assert response.status_code == 200
    assert response.json()['json_data'] == mock_response_data


# sad path 
def test_send_query_wrong_body(client):
    payload = {"message":""}
    payload_dict = dict(payload)
    response = client.post("/send-query", json=payload_dict)
    assert response.status_code == 500

def test_drpc_event_handler_wrong_body(client):
    payload = {  
    "createdAt": "2024-05-15T08:19:38.804Z",
    "request": {
    "jsonrpc": "string",
    "method": "string",
    "params": [
      "string"
    ],
    "id": "string"
  },}
    payload_dict = dict(payload)
    response = client.post("/webhooks/drpc", json=payload_dict)
    assert response.status_code == 422

def test_receive_response_wrong_body(client,mocker):
    payload = {"message":""}
    payload_dict = dict(payload)
    response = client.post("/receive-response", json=payload_dict)
    assert response.status_code == 500

def test_receive_response_wrong_body():

    assert 1+2 == 3