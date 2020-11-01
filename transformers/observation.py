from models import Encounter, Patient, Observation


class ObservationTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def deserialize(self, session):
        patient_src_id = self.raw_data["subject"]["reference"].split("/")[0]
        patient_id = Patient.get_id_for_source_id(session, patient_src_id)

        encounter_src_id = self.raw_data["context"]["reference"].split("/")[0]
        encounter_id = Encounter.get_id_for_source_id(session, encounter_src_id)

        if "component" in self.raw_data:
            components = [
                {"code": component["code"], "valueQuantity": component["valueQuantity"]}
                for component in self.raw_data["components"]
            ]
        else:
            components = [
                {
                    "code": self.raw_data["code"],
                    "valueQuantity": self.raw_data["valueQuantity"],
                }
            ]

        return [
            Observation(
                source_id=self.raw_data["source_id"],
                patient_id=patient_id,
                encounter_id=encounter_id,
                observation_date=self.raw_data["effectiveDateTime"].split("T")[0],
                type_code=component["code"]["coding"][0]["code"],
                type_code_system=component["code"]["coding"][0]["system"],
                value=component["valueQuantity"]["value"],
                unit_code=component["valueQuantity"]["unit"],
                unit_code_system=component["valueQuantity"]["system"],
            )
            for component in components
        ]
