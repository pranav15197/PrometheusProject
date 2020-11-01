from models import Encounter, Patient, Procedure


class ProcedureTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def deserialize(self, session):
        patient_src_id = self.raw_data["subject"]["reference"].split("/")[0]
        patient_id = Patient.get_id_for_source_id(session, patient_src_id)

        encounter_src_id = self.raw_data["context"]["reference"].split("/")[0]
        encounter_id = Encounter.get_id_for_source_id(session, encounter_src_id)
        if "performedDateTime" in self.raw_data:
            procedure_date = self.raw_data["performedDateTime"].split("T")[0]
        else:
            procedure_date = self.raw_data["performedPeriod"]["start"].split("T")[0]
        return Procedure(
            source_id=self.raw_data["id"],
            patient_id=patient_id,
            encounter_id=encounter_id,
            procedure_date=procedure_date,
            type_code=self.raw_data["code"]["coding"][0]["code"],
            type_code_system=self.raw_data["code"]["coding"][0]["system"],
        )
