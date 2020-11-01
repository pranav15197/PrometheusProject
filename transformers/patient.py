from models import Patient


class PatientTransformer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def deserialize(self):
        race_ext, ethnicity_ext = None, None
        for ext in self.raw_data.get("extension", []):
            if (
                ext["url"]
                == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
            ):
                race_ext = ext
            if (
                ext["url"]
                == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
            ):
                ethnicity_ext = ext
        return Patient(
            source_id=self.raw_data["id"],
            birth_date=self.raw_data["birthDate"],
            gender=self.raw_data["gender"],
            country=self.raw_data["address"][0]["country"]
            if "address" in self.raw_data and "country" in self.raw_data["address"][0]
            else None,
            race_code=race_ext["valueCodeableConcept"]["coding"][0]["code"]
            if race_ext
            else None,
            race_code_system=race_ext["valueCodeableConcept"]["coding"][0]["system"]
            if race_ext
            else None,
            ethnicity_code=ethnicity_ext["valueCodeableConcept"]["coding"][0]["code"]
            if ethnicity_ext
            else None,
            ethnicity_code_system=ethnicity_ext["valueCodeableConcept"]["coding"][0][
                "system"
            ]
            if ethnicity_ext
            else None,
        )
