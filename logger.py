import logging.config


class LoggerFacade(object):

    @staticmethod
    def getLogger(foo=0):
        logging.config.fileConfig('logging.conf')
        return logging.getLogger('sbtGenerator')
