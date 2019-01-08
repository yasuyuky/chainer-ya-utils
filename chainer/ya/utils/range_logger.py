import logging


class rangelog:
    logger = None
    startmsg = "--> Start: {name}"
    endmsg = "<--   End:"  # noqa

    @classmethod
    def set_logger(cls, logger=None):
        if logger is None:
            cls.logger = logging.getLogger()
            cls.logger.setLevel(getattr(logging, 'INFO'))
            cls.logger.addHandler(logging.StreamHandler())
        elif isinstance(logger, logging.Logger):
            cls.logger = logger

    @classmethod
    def set_start_msg(cls, msg):
        cls.startmsg = msg

    @classmethod
    def set_end_msg(cls, msg):
        cls.endmsg = msg

    def __init__(self, name):
        if rangelog.logger is None:
            rangelog.set_logger()
        self.name = name

    def __enter__(self):
        rangelog.logger.info(rangelog.startmsg.format(name=self.name))
        return rangelog.logger

    def __exit__(self, *args):
        rangelog.logger.info(rangelog.endmsg.format(name=self.name))
