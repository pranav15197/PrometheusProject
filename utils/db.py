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
    if not engine.dialect.has_table(engine, Patient.__tablename__):
        Patient.__table__.create(engine)
    if not engine.dialect.has_table(engine, Encounter.__tablename__):
        Encounter.__table__.create(engine)
    if not engine.dialect.has_table(engine, Procedure.__tablename__):
        Procedure.__table__.create(engine)
    if not engine.dialect.has_table(engine, Observation.__tablename__):
        Observation.__table__.create(engine)
    engine.dispose()


def drop_all_data(session):
    from models import Patient, Encounter, Observation, Procedure

    Patient.clear_all_records(session)
    Encounter.clear_all_records(session)
    Observation.clear_all_records(session)
    Procedure.clear_all_records(session)

    session.execute(f"DROP INDEX IF EXISTS {Patient.SRC_INDEX}")
    session.execute(f"DROP INDEX IF EXISTS {Encounter.SRC_INDEX}")

    session.commit()
