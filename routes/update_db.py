from fastapi import APIRouter
from schemas.data_form import Data_resync_request
from fastapi import HTTPException
#/////////////Scripts//////////////////////////////////////////
from scripts.UPDB import getdata_smartolt
#/////////////////////////////////////////////////////////////
import os
from dotenv import load_dotenv

load_dotenv()
update_db = APIRouter()

@update_db.get("/update_client_db_status")
def status():
    return HTTPException(status_code=202, detail="UPDB_Running")

@update_db.post("/update_client_db")
def update_client_db(data: Data_resync_request):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = getdata_smartolt(data.data.unique_id_smartolt)
    return HTTPException(status_code=202, detail=response)
