from sqlalchemy import create_engine, MetaData
from ..constants.database import DB_URL


#Connection to Database feelings_app
engine = create_engine(DB_URL)

#Metadata to database
meta = MetaData()

#Connector to database
conn = engine.connect()