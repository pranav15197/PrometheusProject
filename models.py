from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
    DECIMAL,
    Index,
)
from sqlalchemy.orm import relationship
from utils.db import Base


class Patient(Base):
    __tablename__ = "patients"
    SRC_INDEX = "patient_source_id_idx"
    id = Column(Integer, primary_key=True)
    source_id = Column(String(100), unique=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    race_code = Column(String(100), nullable=True)
    race_code_system = Column(String(100), nullable=True)
    ethnicity_code = Column(String(100), nullable=True)
    ethnicity_code_system = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    @staticmethod
    def clear_all_records(session):
        return session.query(Patient).delete()

    @staticmethod
    def get_id_for_source_id(session, source_id):
        return session.query(Patient.id).filter_by(source_id=source_id).scalar()

    @staticmethod
    def create_source_id_index(session):
        engine = session.get_bind()
        patient_source_id_idx = Index(Patient.SRC_INDEX, Patient.source_id)
        patient_source_id_idx.create(engine)
        session.commit()


class Encounter(Base):
    __tablename__ = "encounters"
    SRC_INDEX = "encounter_source_id_idx"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient")
    source_id = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    type_code = Column(String(100), nullable=True)
    type_code_system = Column(String(100), nullable=True)

    @staticmethod
    def clear_all_records(session):
        return session.query(Encounter).delete()

    @staticmethod
    def get_id_for_source_id(session, source_id):
        return session.query(Encounter.id).filter_by(source_id=source_id).scalar()

    @staticmethod
    def create_source_id_index(session):
        engine = session.get_bind()
        patient_source_id_idx = Index(Encounter.SRC_INDEX, Encounter.source_id)
        patient_source_id_idx.create(engine)
        session.commit()


class Procedure(Base):
    __tablename__ = "procedures"
    id = Column(Integer, primary_key=True)
    source_id = Column(String(100), unique=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient")
    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=True)
    encounter = relationship("Patient")
    procedure_date = Column(Date)
    type_code = Column(String(100))
    type_code_system = Column(String(100))

    @staticmethod
    def clear_all_records(session):
        return session.query(Procedure).delete()


class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    source_id = Column(String(100), unique=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient")
    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=True)
    encounter = relationship("Patient")
    observation_date = Column(Date)
    type_code = Column(String(100))
    type_code_system = Column(String(100))
    value = Column(DECIMAL)
    unit_code = Column(String(100), nullable=True)
    unit_code_system = Column(String(100), nullable=True)

    @staticmethod
    def clear_all_records(session):
        return session.query(Observation).delete()
