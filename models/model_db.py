from sqlalchemy import Table,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class get_client(Base):
    __tablename__ = 'clients'

    id = Column('id',Integer(), primary_key=True)
    name = Column('name',String(50))

class client_db(Base):
    __tablename__ = 'db_api_clients'

    contract = Column('contract',String(50),primary_key=True)  
    frame = Column('frame',Integer()) 
    slot = Column('slot',Integer()) 
    port = Column('port',Integer())  
    onu_id = Column('onu_id',Integer()) 
    olt = Column('olt',Integer())  
    fsp = Column('fsp',String(50))  
    fspi = Column('fspi',String(50)) 
    name_1 = Column('name_1',String(50)) 
    name_2 = Column('name_2',String(50)) 
    status = Column('status',String(50),default='online') 
    state = Column('state',String(50)) 
    sn = Column('sn',String(50)) 
    device = Column('device',String(50)) 
    plan_name = Column('plan_name',String(50)) 
    spid = Column('spid',Integer())  


