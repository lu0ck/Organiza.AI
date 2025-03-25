from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONN = "sqlite:///bancodedados.db"

engine = create_engine(CONN, echo=True)
session = sessionmaker(bind=engine)
session = session()
base = declarative_base()

class dados(base):
    __tablename__ = "dados"
    id = Column(Integer, primary_key=True)
    data = Column(String)
    km_total_dia = Column(Float)
    ganho_total_dia = Column(Float)
    gasto_total_dia = Column(Float)

base.metadata.create_all(engine)