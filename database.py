from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Concetar la base de datos entre python y la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Permite actualizar la base de datos
Base = declarative_base()