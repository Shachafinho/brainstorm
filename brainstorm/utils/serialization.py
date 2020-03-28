def object_to_kwargs(obj):
    return {key: getattr(feelings_obj, key) for key in obj.__slots__}
