from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
#////Importando rutas ///////////////////
from routes.resync import resync
from routes.client import client
from routes.wan_config import wan_config

app = FastAPI()

#/////Agregando la ruta al route
app.include_router(resync)
app.include_router(client)
app.include_router(wan_config)


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
    return HTTPException(status_code=202, detail="ms_running")

        # return HTTPException(status_code=401, detail="Invalid API key")
    # {"response":"Cliente no se encuentra en la OLT","status":"OK"}
    # return HTTPException(status_code=404, detail="Client not found in OLT or not instaled")


# @app.post("/resync-ont")
# async def resync_ont(request_data: RequestData):
#     api_key = request_data.api_key
#     unique_id_smartolt = request_data.data.get("unique_id_smartolt")
#     print(request_data)
#     # Do something with the data here
#     return {"message": "Received data successfully"}