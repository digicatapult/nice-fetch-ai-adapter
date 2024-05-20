from fastapi import APIRouter,HTTPException
from typing import Optional, List, Any
from datetime import datetime
from enum import IntEnum, StrEnum
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import requests
from uagents import Model 

veritableUrl = "http://localhost:3010"
peerUrl="http://localhost:3001/api"


class Query(BaseModel):
    message: dict

class DrpcRequestObject(Model):
  jsonrpc: str
  method: str
  params: Optional[List | object]
  id: Optional[str| int ]

class DrpcErrorCode(IntEnum):
  method_not_found = -32601,  
  parse_error = -32700,
  invalid_request = -32600,
  invalid_params = -32602,
  internal_error = -32603,
  server_error = -32000,

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


router = APIRouter()


async def postToVeritable(req:Query)-> JSONResponse:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{veritableUrl}/drcp/request", json=req)
        return [response.status, response.json()]
async def postResponseToVeritable(req: Response)-> JSONResponse:
    async with httpx.AsyncClient() as client:
        response = client.post(f"{veritableUrl}/drcp/response", json=req)
        return [response.status, response.json()]
async def peerReceivesResponse(req: DrpcEvent) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{peerUrl}/receive-response", json=req)
        return [response.status, response.json()]
async def peerReceivesQuery(req: DrpcEvent) -> JSONResponse:
    async with httpx.AsyncClient() as client:
        response =await client.post(f"{peerUrl}/receive-query", json=req)
        return [response.status, response.json()]
            
@router.post("/send-query", name="test-name",status_code=202)
async def send_query(req: Query): # need to define Query 
    try:
        response = await postToVeritable(req)
        if response[0] != '202':
            raise ValueError("Response status is not 202")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/webhooks/drpc", name="webhooks-drpc",status_code=200) #from veritable cloudagent to peerAPI
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
        request_check = req_dict['request']
        response_check = req_dict['response']
        role_check = req_dict['role']
        if request_check and response_check:
            raise ValueError("JSON body cannot contain both 'request' and 'response'")
        if request_check and role_check != 'server':
            raise ValueError("If 'request' is present, 'role' must be 'server'")
        if response_check and role_check != 'client':
            raise ValueError("If 'response' is present, 'role' must be 'client'")
        if role_check =='client': 
            response =await  peerReceivesResponse(req_dict)
        elif role_check =='server': 
            response = await peerReceivesQuery(req_dict)
        else:
            raise ValueError("Error in request body.")
        if response[0] != '200':
            raise ValueError("Response status is not 200")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/receive-response", name="receive-response",status_code=200)  ## this receives response from chainvine and it forwards info to veritable 
async def receive_response(resp: Response): #basic RPC response 
    try:
        response = await postResponseToVeritable(resp)
        if response[0] != '200':
            raise ValueError("Response status is not 200")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))