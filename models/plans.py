from sqlalchemy import Table,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class plans_db(Base):
    __tablename__ = 'db_api_plans'

    plan_name = Column('plan_name',String(50),primary_key=True)  
    plan_idx = Column('plan_idx',Integer()) 
    srv_profile = Column('srv_profile',Integer()) 
    line_profile = Column('line_profile',Integer())  
    gem_port = Column('gem_port',Integer()) 
    provider = Column('provider',String(50))  
    vlan = Column('vlan',Integer())  

