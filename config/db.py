from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from models.model_db import client_db


load_dotenv()

engine = create_engine(f"postgresql+psycopg2://tg_conext:conext123@54.186.94.225:5432/conext")
engine.echo = True 
conn = engine.connect()

Session = sessionmaker(engine)
session = Session()



# returned = session.query(client_db).filter(client_db.contract == '0050000209').first()

# if returned == None:
#     print("No existe")
# else:
#     print(returned)

# returned.name_1 = 'YUGLENIS'
# session.add(returned)
# session.commit()