from sqlalchemy import desc, func, extract
from utils.db import get_session, init_db
from utils.ndjson_reader import NDJsonReader
from transformers.patient import PatientTransformer
from transformers.encounter import EncounterTransformer
from transformers.observation import ObservationTransformer
from transformers.procedure import ProcedureTransformer
from models import Patient, Encounter, Observation, Procedure

if __name__ == "__main__":
    session = get_session()
    # create tables if they don't exist
    print("Creating Tables..")
    init_db()

    # First clear all records
    print("Removing Existing Data..")
    Patient.clear_all_records(session)
    Encounter.clear_all_records(session)
    Observation.clear_all_records(session)
    Procedure.clear_all_records(session)
    session.commit()

    # Import Patients
    print("Importing Patient Data..")
    reader = NDJsonReader("data/patients.ndjson")
    data_dicts = reader.parse_rows()
    print("Bad rows in patients:", len(reader.bad_rows))
    patients = [PatientTransformer(data_dict).deserialize() for data_dict in data_dicts]
    session.bulk_save_objects(patients)
    session.commit()

    # # Import Encounters
    print("Importing Encounter Data..")
    reader = NDJsonReader("data/encounters.ndjson")
    data_dicts = reader.parse_rows()
    print("Bad rows in encounters:", len(reader.bad_rows))
    encounters = [
        EncounterTransformer(data_dict).deserialize(session) for data_dict in data_dicts
    ]
    session.bulk_save_objects(encounters)
    session.commit()

    # Import Observations
    print("Importing Observation Data..")
    reader = NDJsonReader("data/observations.ndjson")
    data_dicts = reader.parse_rows()
    print("Bad rows in observations:", len(reader.bad_rows))
    observations = []
    for data_dict in data_dicts:
        observations.extend(ObservationTransformer(data_dict).deserialize(session))
    session.bulk_save_objects(observations)
    session.commit()

    # Import Procedures
    print("Importing Procedure Data..")
    reader = NDJsonReader("data/procedures.ndjson")
    data_dicts = reader.parse_rows()
    print("Bad rows in procedures:", len(reader.bad_rows))
    procedures = [
        ProcedureTransformer(data_dict).deserialize(session) for data_dict in data_dicts
    ]
    session.bulk_save_objects(procedures)
    session.commit()
    print("All Data imported!")

    print("===" * 10)
    print("REPORT")
    print("---" * 10)
    # Now generating report

    print(f"{'Patients added':>20}", ":", session.query(Patient.id).count())
    print(f"{'Encounters added':>20}", ":", session.query(Encounter.id).count())
    print(f"{'Procedures added':>20}", ":", session.query(Procedure.id).count())
    print(f"{'Observations added':>20}", ":", session.query(Observation.id).count())

    print("---" * 10)
    print("Patients By Gender")
    print("")
    gender_groups = (
        session.query(Patient.gender, func.count(Patient.gender))
        .group_by(Patient.gender)
        .all()
    )
    for gender, count in gender_groups:
        print(f"{gender:>20} : {count}")

    print("---" * 10)
    print("Top Procedures")
    print("")
    top_procedures = (
        session.query(
            Procedure.type_code, func.count(Procedure.type_code).label("count")
        )
        .group_by(Procedure.type_code)
        .order_by(desc("count"))
        .limit(10)
        .all()
    )

    print(f"{'type_code':>20} : {'count'}")
    for procedure_type_code, count in top_procedures:
        print(f"{procedure_type_code:>20} : {count}")

    print("---" * 10)
    weekly_encounters = (
        session.query(
            extract("dow", Encounter.start_date).label("dow"),
            func.count(extract("dow", Encounter.start_date)).label("count"),
        )
        .group_by("dow")
        .order_by(desc("count"))
        .all()
    )
    print("Day with most encounters:", weekly_encounters[0][0])
    print("Day with least encounters:", weekly_encounters[-1][0])
    print("---" * 10)
    session.close()