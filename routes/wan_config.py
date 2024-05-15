from fastapi import APIRouter
from models.data_form import Data_resync_request
from fastapi import HTTPException
#/////////////Scripts//////////////////////////////////////////
from scripts.WC import wanconfig_getdata_smartolt
#/////////////////////////////////////////////////////////////
import os
from dotenv import load_dotenv

load_dotenv()
wanconfig = APIRouter()

@wanconfig.get("/wan-config-status")
def status():
    return HTTPException(status_code=202, detail="WC_Running")

@wanconfig.post("/wan-config-ont")
def wan_config(data: Data_resync_request):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = wanconfig_getdata_smartolt(data.data.unique_id_smartolt)
    return HTTPException(status_code=202, detail=response)
