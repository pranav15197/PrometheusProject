from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from utils.db import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    source_id = Column(String(100))
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    race_code = Column(String(100), nullable=True)
    race_code_system = Column(String(100), nullable=True)
    ethnicity_code = Column(String(100), nullable=True)
    ethnicity_code_system = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)


class Encounter(Base):
    __tablename__ = "encounters"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient")
    source_id = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    type_code = Column(String(100), nullable=True)
    type_code_system = Column(String(100), nullable=True)


class Procedure(Base):
    __tablename__ = "procedures"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient")
    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=True)
    encounter = relationship("Patient")
    procedure_date = Column(Date)
    type_code = Column(String(100))
    type_code_system = Column(String(100))


class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
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
