import json
from typing import Optional, List, Any
from datetime import datetime
from enum import IntEnum, StrEnum
import requests
from fastapi import FastAPI, HTTPException
from uagents import Model
from uagents.query import query


 
veritableUrl = "http://localhost:3010"
peerUrl="http://localhost:3001/api"
 
class TestRequest(Model):
    message: str

class DrpcRequestObject(Model):
  jsonrpc: str
  method: str
  params: Optional[List | object]
  id: Optional[str| int ]

class DrpcErrorCode(IntEnum):
  METHOD_NOT_FOUND = -32601,  # make all stuff inside enums lowercase 
  PARSE_ERROR = -32700,
  INVALID_REQUEST = -32600,
  INVALID_PARAMS = -32602,
  INTERNAL_ERROR = -32603,
  SERVER_ERROR = -32000,

class DrpcResponseError(Model):
  code: DrpcErrorCode
  message: str
  data: Optional[Any]

class DrpcResponseObject(Model):
  jsonrpc: str
  result: Optional[Any]
  error: Optional[DrpcResponseError]
  id: Optional[str| int ]

class DrpcRole(StrEnum):
  Client = 'client',
  Server = 'server',

class DrpcState(StrEnum):
  RequestSent = 'request-sent',
  RequestReceived = 'request-received',
  Completed = 'completed',

class Query(Model):
    message: dict

# RPC Response example 
# --> {"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}
# <-- {"jsonrpc": "2.0", "result": -19, "id": 2}
class Response(Model):
    message: dict

class DrpcEvent(Model):
    createdAt: datetime
    request: Optional[DrpcRequestObject| List[DrpcRequestObject]]
    response: Optional[DrpcResponseObject]
    connectionId: str
    role: DrpcRole
    state: DrpcState
    threadId: str
    id:str
    _tags:dict
 
app = FastAPI()
 
@app.post("/send-query")
async def send_query(req: Query): # need to define Query 
    try:
        req_dict = dict(req)
        #  relay stuff to the drcp/request in veritable
        response = requests.post(f"{veritableUrl}/drcp/request", json=req_dict)
        if response.status_code != 202:
            print("Error:", response.status_code) 
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/webhooks/drpc") #from veritable cloudagent # need to pay attention to responseState changed and request state changed 
async def drpc_event_handler(req: DrpcEvent):
    try:
        req_dict = dict(req)
        req_dict['createdAt'] = req_dict['createdAt'].isoformat()
        
        # Convert DrpcRequestObject object to a dictionary
        if req_dict['request']:
            req_dict['request'] = dict(req_dict['request'])
        
        # Convert DrpcResponseObject object to a dictionary
        if req_dict['response']:
            req_dict['response'] = dict(req_dict['response'])
            # Convert DrpcResponseError object to a dictionary
            if req_dict['response']['error']:
                req_dict['response']['error'] = dict(req_dict['response']['error'])
        if req_dict['role']=='client': 
        # respond to the peer API
            response = requests.post(f"{peerUrl}/receive-response", json=req_dict)
            print('in request')
        if req_dict['role']=='server': 
            response = requests.post(f"{peerUrl}/receive-query", json=req_dict)
        if response.status_code != 200:
            print("Error:", response.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/receive-response")  ## this receives response from chainvine and it forwards info to veritable 
async def receive_response(resp: Response): #basic RPC response 
    try:
        req_dict = dict(resp)
        #  relay stuff to the drcp/response in veritable
        response = requests.post(f"{veritableUrl}/drcp/response", json=req_dict)
        if response.status_code != 200:
            print("Error:", response.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# def start():
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     start()