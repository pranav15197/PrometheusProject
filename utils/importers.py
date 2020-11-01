from utils.ndjson_reader import NDJsonReader


def deserialize_and_save(session, json_name, transformer_class):
    """
    Works for Patient, Encounter, Procedure
    """
    reader = NDJsonReader(f"data/{json_name}.ndjson")
    data_dicts = reader.parse_rows()
    objects = []
    for data_dict in data_dicts:
        transformer = transformer_class(data_dict)
        if not transformer.validate():
            # Skipping this data
            continue
        try:
            objects.append(transformer.deserialize(session))
        except Exception:
            # unknown error while deserializing
            # TODO - Better validation here
            continue

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
        transformer = transformer_class(data_dict)
        if not transformer.validate():
            # Skipping this data
            continue
        try:
            objects.extend(transformer.deserialize(session))
        except Exception:
            # unknown error while deserializing
            # TODO - Better validation here
            continue
    session.bulk_save_objects(objects)
    session.commit()
