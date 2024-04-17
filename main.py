from fastapi import FastAPI
from models.data_form import Data_request,Data_resync_request
from scripts.IC import search_autofind
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from utils.request import db_request_smartolt
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

origins = [
    "http://localhost",
    "http://localhost:49229",
    "http://127.0.0.1",
    "http://127.0.0.1:49229",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "10.7.110.233:8000",
    "10.7.110.233:3000",
    "10.7.110.233"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add-client")
def add_data(data: Data_request):
    # Api key MS operativos ---------------------- 
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    complete_contract = data.data.contract.zfill(10)
    response = search_autofind(data.data.name,complete_contract,data.data.olt,data.data.sn,data.data.device_type,data.data.assigned_public_ip,data.data.plan_name,data.data.isbridge)
    return HTTPException(status_code=202, detail=response)
        # return HTTPException(status_code=401, detail="Invalid API key")
    # {"response":"Cliente no se encuentra en la OLT","status":"OK"}
    # return HTTPException(status_code=404, detail="Client not found in OLT or not instaled")

@app.post("/resync-ont")
def add_data(data: Data_resync_request):
    # Api key smartolt ----------------------
    if data.api_key != os.environ["API_KEY_SMARTOLT"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = db_request_smartolt('get_onu_smartolt','HWTCEF11529F')
    return HTTPException(status_code=202, detail="yes")
