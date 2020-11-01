from models import Encounter, Patient


class EncounterTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def validate(self):
        try:
            self.raw_data["id"]
            self.raw_data["period"]["start"]
            self.raw_data["period"]["end"]
            self.raw_data["subject"]["reference"]
        except KeyError:
            return False
        return True

    def deserialize(self, session):
        patient_src_id = self.raw_data["subject"]["reference"].split("/")[0]
        patient_id = Patient.get_id_for_source_id(session, patient_src_id)
        return Encounter(
            source_id=self.raw_data["id"],
            patient_id=patient_id,
            start_date=self.raw_data["period"]["start"],
            end_date=self.raw_data["period"]["end"],
            type_code=self.raw_data["type"][0]["coding"][0]["code"],
            type_code_system=self.raw_data["type"][0]["coding"][0]["system"],
        )
