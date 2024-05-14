from fastapi import APIRouter
from models.data_form import Data_resync_request
from fastapi import HTTPException
#/////////////Scripts//////////////////////////////////////////
from scripts.RS import resync_getdata_smartolt
#/////////////////////////////////////////////////////////////
import os
from dotenv import load_dotenv

load_dotenv()
resync = APIRouter()

@resync.get("/resync-status")
def status():
    return HTTPException(status_code=202, detail="RS_Running")

@resync.post("/resync-ont")
def add_data(data: Data_resync_request):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = resync_getdata_smartolt(data.data.unique_id_smartolt)
    return HTTPException(status_code=202, detail=response)
