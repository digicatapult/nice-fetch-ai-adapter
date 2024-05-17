# from fastapi import FastAPI, HTTPException, Depends
# import httpx
# from typing import Any
# from pydantic import BaseModel

# veritableUrl = "http://localhost:3010"
# peerUrl = "http://localhost:3001/api"

# app = FastAPI()
# class Query(BaseModel):
#     message: dict

# def get_http_client() -> httpx.AsyncClient:
#     return httpx.AsyncClient()

# @app.post("/send-query")
# async def send_query(req: Query, http_client: httpx.AsyncClient = Depends(get_http_client)):
#     try:
#         response = await http_client.post(f"{veritableUrl}/drcp/request", json=req)
#         if response.status_code != 202:
#             print("Error:", response.status_code)
#         return response.json()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # Other endpoints ...
