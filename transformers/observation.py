from models import Encounter, Patient, Observation


class ObservationTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def validate(self):
        try:
            self.raw_data["id"]
            self.raw_data["effectiveDateTime"]
            self.raw_data["subject"]["reference"]
            self.raw_data["context"]["reference"]
        except KeyError:
            return False
        return True

    def deserialize(self, session):
        patient_src_id = self.raw_data["subject"]["reference"].split("/")[0]
        patient_id = Patient.get_id_for_source_id(session, patient_src_id)

        encounter_src_id = self.raw_data["context"]["reference"].split("/")[0]
        encounter_id = Encounter.get_id_for_source_id(session, encounter_src_id)

        if "component" in self.raw_data:
            components = [
                {"code": component["code"], "valueQuantity": component["valueQuantity"]}
                for component in self.raw_data["component"]
            ]
        else:
            components = [
                {
                    "code": self.raw_data["code"],
                    "valueQuantity": self.raw_data.get("valueQuantity", None),
                }
            ]

        return [
            Observation(
                source_id=self.raw_data["id"] + "-" + str(i),
                patient_id=patient_id,
                encounter_id=encounter_id,
                observation_date=self.raw_data["effectiveDateTime"].split("T")[0],
                type_code=component["code"]["coding"][0]["code"],
                type_code_system=component["code"]["coding"][0]["system"],
                value=component["valueQuantity"]["value"]
                if component["valueQuantity"]
                else None,
                unit_code=component["valueQuantity"]["unit"]
                if component["valueQuantity"]
                else None,
                unit_code_system=component["valueQuantity"]["system"]
                if component["valueQuantity"]
                else None,
            )
            for i, component in enumerate(components)
        ]
