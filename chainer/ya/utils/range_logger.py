import logging

logger = logging.getLogger()
logger.setLevel(getattr(logging, 'INFO'))
logger.addHandler(logging.StreamHandler())


class rangelog:

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        logger.info("--> Start: {}".format(self.name))
        return logger

    def __exit__(self, *args):
        logger.info("<-- End: {}".format(self.name))
