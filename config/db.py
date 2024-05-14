from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.model_db import Base

engine = create_engine("postgresql+psycopg2://tg_conext:conext123@54.186.94.225:5432/conext")

# conn = engine.connect()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()