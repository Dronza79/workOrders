import logging


def add_logger_peewee(fun):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return fun(*args, **kwargs)
    return wrapper

