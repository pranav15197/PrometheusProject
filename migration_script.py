from utils.db import get_session, init_db, drop_all_data
from utils.importers import deserialize_and_save, deserialize_and_save_observations
from utils.report import (
    generate_data_size_report,
    generate_gender_report,
    generate_procedures_report,
    generate_encounters_report,
)
from transformers.patient import PatientTransformer
from transformers.encounter import EncounterTransformer
from transformers.observation import ObservationTransformer
from transformers.procedure import ProcedureTransformer
from models import Patient, Encounter


if __name__ == "__main__":
    session = get_session()
    engine = session.get_bind()
    # create tables if they don't exist
    print("Creating Tables..")
    init_db()

    # First clear all records
    print("Removing Existing Data..")
    drop_all_data(session)

    # Import Patients
    print("Importing Data..")
    deserialize_and_save(session, "patients", PatientTransformer)
    Patient.create_source_id_index(session)

    deserialize_and_save(session, "encounters", EncounterTransformer)
    Encounter.create_source_id_index(session)

    deserialize_and_save(session, "procedures", ProcedureTransformer)

    deserialize_and_save_observations(session, "observations", ObservationTransformer)

    session.commit()
    print("All Data imported!")

    print("===" * 20)
    print("REPORT")
    generate_data_size_report(session)
    generate_gender_report(session)
    generate_procedures_report(session)
    generate_encounters_report(session)
    print("===" * 20)
    session.close()
