import os
from render import www


def path_for(name):
    paths = os.path.abspath(www.__file__).replace("/__init__.py", "").split("/")
    paths.append(name)
    return "/".join(paths)
