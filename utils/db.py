from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()  # Base class used by other models
USERNAME = "postgres"
PASSWORD = "testing"
HOST = "localhost"
DB = "prometheus"


def get_db_engine():
    engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}/{DB}")
    return engine


def get_session():
    engine = get_db_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


def init_db():
    from models import Patient, Encounter, Procedure, Observation

    engine = get_db_engine()
    Patient.__table__.create(engine)
    Encounter.__table__.create(engine)
    Procedure.__table__.create(engine)
    Observation.__table__.create(engine)
    engine.dispose()
