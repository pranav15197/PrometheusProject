from sqlalchemy import desc, func, extract
from utils.db import get_session
from utils.ndjson_reader import NDJsonReader
from transformers.patient import PatientTransformer
from transformers.encounter import EncounterTransformer
from transformers.observation import ObservationTransformer
from transformers.procedure import ProcedureTransformer
from models import Patient, Encounter, Observation, Procedure


session = get_session()


# First clear all records
Patient.clear_all_records(session)
Encounter.clear_all_records(session)
Observation.clear_all_records(session)
Procedure.clear_all_records(session)
session.commit()

# Import Patients
reader = NDJsonReader("data/patients.ndjson")
data_dicts = reader.parse_rows()
patients = [PatientTransformer(data_dict).deserialize() for data_dict in data_dicts]
session.bulk_save_objects(patients)
session.commit()

# # Import Encounters
reader = NDJsonReader("data/encounters.ndjson")
data_dicts = reader.parse_rows()
encounters = [
    EncounterTransformer(data_dict).deserialize(session) for data_dict in data_dicts
]
session.bulk_save_objects(encounters)
session.commit()

# Import Observations
reader = NDJsonReader("data/observations.ndjson")
data_dicts = reader.parse_rows()
observations = []
for data_dict in data_dicts:
    observations.extend(ObservationTransformer(data_dict).deserialize(session))
session.bulk_save_objects(observations)
session.commit()

# Import Procedures
reader = NDJsonReader("data/procedures.ndjson")
data_dicts = reader.parse_rows()
procedures = [
    ProcedureTransformer(data_dict).deserialize(session) for data_dict in data_dicts
]
session.bulk_save_objects(procedures)
session.commit()

print("Patients added:", session.query(Patient.id).count())
print("Encounters added:", session.query(Encounter.id).count())
print("Procedures added:", session.query(Procedure.id).count())
print("Observations added:", session.query(Observation.id).count())

print(
    session.query(Patient.gender, func.count(Patient.gender))
    .group_by(Patient.gender)
    .all()
)

print(
    session.query(Procedure.type_code, func.count(Procedure.type_code).label("count"))
    .group_by(Procedure.type_code)
    .order_by(desc("count"))
    .limit(10)
    .all()
)


print(
    session.query(
        extract("dow", Encounter.start_date).label("dow"),
        func.count(extract("dow", Encounter.start_date)).label("count"),
    )
    .group_by("dow")
    .order_by(desc("count"))
    .all()
)


session.close()