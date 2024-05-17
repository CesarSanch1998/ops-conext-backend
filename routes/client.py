from fastapi import APIRouter
from schemas.data_form import Data_request
from fastapi import HTTPException
#/////////////////////////////////////////////////
import os
from dotenv import load_dotenv
from scripts.IC import search_autofind


client = APIRouter()
@client.get("/client-status")
def status():
    return HTTPException(status_code=202, detail="RS_Running")

@client.post("/add-client")
def add_data(data: Data_request):
    # Api key MS operativos ---------------------- 
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    complete_contract = data.data.contract.zfill(10)
    response = search_autofind(data.data.name,complete_contract,data.data.olt,data.data.sn,data.data.device_type,data.data.assigned_public_ip,data.data.plan_name,data.data.isbridge)
    return HTTPException(status_code=202, detail=response)