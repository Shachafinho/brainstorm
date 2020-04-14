import arrow
import cattr


converter = cattr.Converter()
converter.register_unstructure_hook(
    arrow.Arrow, lambda a: a.for_json())
converter.register_structure_hook(
    arrow.Arrow, lambda timestamp_str, _: arrow.get(timestamp_str))
