#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print("Create sqlite database")
engine = create_engine(
    "sqlite:///complexityweekend.sqlite",
    connect_args={'check_same_thread': False}
    )
## Also same thread is from https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa

Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=False)
## auto flush was added because of https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy

session = Session()

class Messages(Base):
    __tablename__ = "UserSessions"
    id = Column(Integer, primary_key=True)
    team = Column(String(1024))
    topic = Column(String(128))
    msg_id = Column(Integer)
    msg_type = Column(String(32))
    from_user = Column(String(128))
    sent_time = Column(Integer)
    txt_body = Column(String(4096))
    reaction_body = Column(String(1024))
    reaction_reference = Column(Integer)

def CreateDatabase():
    Base.metadata.create_all(engine)

CreateDatabase()
