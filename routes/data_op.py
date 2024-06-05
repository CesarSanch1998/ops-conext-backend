from fastapi import APIRouter
from schemas.data_form import Data_resync_request
from fastapi import HTTPException
#/////////////Scripts//////////////////////////////////////////
from scripts.DOP import getdata_smartolt
#/////////////////////////////////////////////////////////////
import os
from dotenv import load_dotenv

load_dotenv()
data_op = APIRouter()



@data_op.post("/get-data-op")
def get_data_op_db(data: Data_resync_request):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = getdata_smartolt(data.data.unique_id_smartolt)
    return HTTPException(status_code=202, detail=response)
