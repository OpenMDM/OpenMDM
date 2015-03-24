def str_to_bool(s):
    if type(s) == "bool":
        return s
    return s.lower() in ("yes", "true", "t", "y", "1")