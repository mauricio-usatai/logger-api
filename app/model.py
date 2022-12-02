from sqlalchemy import (
  Integer,
  String,
  Column,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Log(Base):
  __abstract__ = True
  __table_args__ = { 'extend_existing': True }
  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(Integer)
  level = Column(String(10))
  log_message = Column(String(5000))