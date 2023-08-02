from datetime import datetime, timedelta
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
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        response = Response(_source_language, _target_language, _api_used, _success)
        session.add(response)
        session.commit()


class Recommendation:
    @classmethod
    def recommendation(cls):
        engine = create_engine("sqlite:///database.db", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        one_hour_ago = datetime.utcnow() - timedelta(hours=1)

        responses = session.query(Response.api_used, Response.success). \
            filter(Response.timestamp >= one_hour_ago).all()

        session.close()
        return responses

    @classmethod
    def highest_success_api(cls):
        result=cls.recommendation()
        api_total_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}
        api_successful_attempts = {'google': 0, 'lacto': 0, 'rapid': 0}

        for row in result:
            api, success = row
            if api in api_total_attempts:
                api_total_attempts[api] += 1
                if success == 1:
                    api_successful_attempts[api] += 1

        api_success_rates = {
            'google': api_successful_attempts['google'] / api_total_attempts['google'] if api_total_attempts[
                                                                                              'google'] != 0 else 0,
            'lacto': api_successful_attempts['lacto'] / api_total_attempts['lacto'] if api_total_attempts[
                                                                                           'lacto'] != 0 else 0,
            'rapid': api_successful_attempts['rapid'] / api_total_attempts['rapid'] if api_total_attempts[
                                                                                           'rapid'] != 0 else 0
        }

        highest_success_rate_api = "google"
        max_success=api_success_rates['google']

        for key, value in api_success_rates.items():
            if value > max_success:
                max_success = value
                highest_success_rate_api = key

        response = {'api': "{}".format(highest_success_rate_api.title())}
        return response

