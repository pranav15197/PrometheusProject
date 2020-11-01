from utils.ndjson_reader import NDJsonReader


def deserialize_and_save(session, json_name, transformer_class):
    """
    Works for Patient, Encounter, Procedure
    """
    reader = NDJsonReader(f"data/{json_name}.ndjson")
    data_dicts = reader.parse_rows()
    objects = [
        transformer_class(data_dict).deserialize(session) for data_dict in data_dicts
    ]
    session.bulk_save_objects(objects)
    session.commit()


def deserialize_and_save_observations(session, json_name, transformer_class):
    """
    Works for Observation
    """
    reader = NDJsonReader(f"data/{json_name}.ndjson")
    data_dicts = reader.parse_rows()
    objects = []
    for data_dict in data_dicts:
        objects.extend(transformer_class(data_dict).deserialize(session))
    session.bulk_save_objects(objects)
    session.commit()
