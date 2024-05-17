from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx

veritableUrl = "http://localhost:3010"

class Query(BaseModel):
    message: dict


router = APIRouter()


async def postToVeritable(req:Query)-> JSONResponse:
        req_dict = dict(req)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{veritableUrl}/drcp/request", json=req_dict)
            return response
          
@router.post("/send-query", name="test-name",status_code=202)
async def send_query(req: Query): # need to define Query 
    try:
        response = await postToVeritable(req)
        if response.status_code != 202:
            print("Error:", response.status_code) 
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# @app.post("/webhooks/drpc") #from veritable cloudagent # need to pay attention to responseState changed and request state changed 
# async def drpc_event_handler(req: DrpcEvent):
#     try:
#         req_dict = dict(req)
#         req_dict['createdAt'] = req_dict['createdAt'].isoformat()
        
#         # Convert DrpcRequestObject object to a dictionary
#         if req_dict['request']:
#             req_dict['request'] = dict(req_dict['request'])
        
#         # Convert DrpcResponseObject object to a dictionary
#         if req_dict['response']:
#             req_dict['response'] = dict(req_dict['response'])
#             # Convert DrpcResponseError object to a dictionary
#             if req_dict['response']['error']:
#                 req_dict['response']['error'] = dict(req_dict['response']['error'])
#         if req_dict['role']=='client': 
#         # respond to the peer API
#             response = requests.post(f"{peerUrl}/receive-response", json=req_dict)
#             print('in request')
#         if req_dict['role']=='server': 
#             response = requests.post(f"{peerUrl}/receive-query", json=req_dict)
#         if response.status_code != 200:
#             print("Error:", response.status_code)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @app.post("/receive-response")  ## this receives response from chainvine and it forwards info to veritable 
# async def receive_response(resp: Response): #basic RPC response 
#     try:
#         req_dict = dict(resp)
#         #  relay stuff to the drcp/response in veritable
#         response = requests.post(f"{veritableUrl}/drcp/response", json=req_dict)
#         if response.status_code != 200:
#             print("Error:", response.status_code)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))