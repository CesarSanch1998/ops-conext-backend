from pydantic import BaseModel

class Data(BaseModel):
    id:int
    name: str
    contract: str
    olt: int
    sn: str
    device_type: str
    isbridge:bool
    assigned_public_ip: str
    plan_name: str

class Data_request(BaseModel):
    api_key:str
    type:str
    data:Data

# Format Model to resync Request -----------------------------
class Data_resync(BaseModel):
    unique_id_smartolt:str

class Data_resync_request(BaseModel):
    api_key:str
    data:Data_resync