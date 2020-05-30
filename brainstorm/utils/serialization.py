def object_to_kwargs(obj):
    """Return an object's slots as keyword arguments.

    Arg:
        obj (object): An object with ``__slots__``.

    Return:
        dict(str, object):
          The object's slots as keyword arguments.
          This is a mapping from the slots' names to their respective values.
    """
    return {key: getattr(obj, key) for key in obj.__slots__}
