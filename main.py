from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from models.data_form import Data_request,Data_resync_request,RequestData
from scripts.IC import search_autofind
from scripts.RS import resync_getdata_smartolt
from fastapi import HTTPException
import ssl
import os
from dotenv import load_dotenv

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
load_dotenv()
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain('/home/conext/cert.pem', keyfile='/home/conext/key.pem')

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
    "10.7.110.233",
    "https://conext.smartolt.com"
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
    return {"ms_running"}


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

@app.post("/resync-ont2")
def add_data(data: Data_resync_request):
    # Api key smartolt ----------------------
    print(data)
    if data.api_key != os.environ["API_KEY"]:
        return HTTPException(status_code=401, detail="Invalid API key")
    
    response = resync_getdata_smartolt(data.data.unique_id_smartolt)
    return HTTPException(status_code=202, detail=response)

@app.post("/resync-ont")
async def resync_ont(request_data: RequestData):
    api_key = request_data.api_key
    unique_id_smartolt = request_data.data.get("unique_id_smartolt")
    print(request_data)
    # Do something with the data here
    return {"message": "Received data successfully"}