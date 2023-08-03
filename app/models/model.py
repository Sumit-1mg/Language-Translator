from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Response(Base):
    __tablename__ = "response"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    source_language = Column("source_language", String)
    target_language = Column("target_language", String)
    api_used = Column("api_used", String)
    success = Column("success", Integer)
    timestamp = Column("timestamp", DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, _source_language, _target_language, _api_used, _success):
        self.source_language = _source_language
        self.target_language = _target_language
        self.api_used = _api_used
        self.success = _success

    def __repr__(self):
        return f"({self.api_used} {self.success})"


class SaveResponse:

    @classmethod
    def save(cls,_source_language, _target_language, _api_used, _success):
        engine = create_engine("sqlite:///database.db", echo=True)
        #Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        response = Response(_source_language, _target_language, _api_used, _success)
        session.add(response)
        session.commit()


