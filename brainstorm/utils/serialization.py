def object_to_kwargs(obj):
    return {key: getattr(obj, key) for key in obj.__slots__}
