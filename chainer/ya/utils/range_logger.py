import logging


class rangelog:
    logger = None
    startlog = "--> Start: {name}"
    endlog   = "<--   End:" # noqa

    @classmethod
    def set_logger(cls, logger=None):
        if logger is None:
            cls.logger = logging.getLogger()
            cls.logger.setLevel(getattr(logging, 'INFO'))
            cls.logger.addHandler(logging.StreamHandler())
        elif isinstance(logger, logging.Logger):
            cls.logger = logger

    def __init__(self, name):
        if rangelog.logger is None:
            rangelog.set_logger()
        self.name = name

    def __enter__(self):
        rangelog.logger.info(rangelog.startlog.format(name=self.name))
        return rangelog.logger

    def __exit__(self, *args):
        rangelog.logger.info(rangelog.endlog.format(name=self.name))
