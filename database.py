#!/usr/bin/python3
import os
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Messages(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True)
    team = Column(String(1024))
    topic = Column(String(128))
    msg_id = Column(Integer)
    msg_type = Column(String(32))
    from_user = Column(String(128))
    sent_time = Column(DateTime, default=None)
    txt_body = Column(String(4096))
    word_count = Column(Integer)
    num_urls = Column(Integer)
    urls = Column(String(4096))
    reaction_body = Column(String(1024))
    msg_reference = Column(Integer)
    userMentions = Column(String(1024))

    def __repr__(self):
        return "<Message(id='%d', team='%s', topic='%s', type='%s', from='%s')>" % (self.id, self.team, self.topic, self.msg_type, self.from_user)

class DB(object):
    def __init__(self, database_url):
        engine = create_engine(
            database_url,
            connect_args={'check_same_thread': False},
            echo=False
            )
        ## Echo is only fro debug
        ## Also same thread is from https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine, autoflush=False)
        ## auto flush was added because of https://stackoverflow.com/questions/32922210/why-does-a-query-invoke-a-auto-flush-in-sqlalchemy

        self.session = Session()

