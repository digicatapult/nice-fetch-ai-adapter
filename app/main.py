from typing import Optional, List, Any
from datetime import datetime
from enum import IntEnum, StrEnum
import requests
from fastapi import FastAPI, HTTPException
from uagents import Model
import httpx 
 
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


    
# def start():
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     start()