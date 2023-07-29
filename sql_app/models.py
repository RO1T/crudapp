from sqlalchemy import Column, Integer, String

from .database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Integer)
    link = Column(String)
    datetime = Column(String)


