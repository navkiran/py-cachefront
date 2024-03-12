from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from utils.database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))


Base.metadata.create_all(engine)
print("Database tables created successfully")
