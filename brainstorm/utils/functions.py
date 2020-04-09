import inspect
import re


def get_module_functions(module, pattern):
    return {name: obj for name, obj in inspect.getmembers(module)
            if inspect.isfunction(obj) and re.match(pattern, name)}
