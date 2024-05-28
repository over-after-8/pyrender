def logging_setting() -> None:
    from render.utils.config import config
    import logging

    logging_level = config["logging"]["level"]

    logging.basicConfig(level=logging_level,
                        format=config["logging"]["format"],
                        datefmt='%Y-%m-%d %H:%M:%S')
