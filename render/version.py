import importlib_metadata as metadata

name = "render"

try:
    version = metadata.version(name)
except metadata.PackageNotFoundError as e:
    import logging

    logging.error(e)

    logging.warning(f"No module named {name}")