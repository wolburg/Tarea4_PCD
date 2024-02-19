from sqlalchemy import Column, Integer, String
from database import Base

#Definir esquema de la tabla: datos y columnas
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)
    recommendations = Column(String)
    ZIP = Column(String)
