from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_uuid = Column(String, unique=True, nullable=False)
    balance = Column(Integer, default=1000)
