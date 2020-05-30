import inspect
import re


def get_module_functions(module, pattern):
    """Return all functions of the specified module matching the pattern.

    Args:
        module (module): A module whose functions are scanned.
        pattern (str): A pattern against which the function names are matched.

    Return:
        dict(str, func):
          The module's functions matching the pattern.
          This is a mapping from functions' names to their respective objects.
    """
    return {name: obj for name, obj in inspect.getmembers(module)
            if inspect.isfunction(obj) and re.match(pattern, name)}
