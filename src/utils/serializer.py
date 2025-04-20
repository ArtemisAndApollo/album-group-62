def serialize_similarity_modes(similarity_modes):
    serializable = {}
    for key, value in similarity_modes.items():
        sim_func_name = type(value['sim_function']).__name__
        serializable[key] = {
            "sim_function": sim_func_name,
            "threshold": value["threshold"]
        }
    return serializable