import logging.config


class LoggerFacade(object):

    @staticmethod
    def clear_log_file():
        with open('sbtScala.log', 'w'):
            pass

    @staticmethod
    def getLogger(foo=0):
        logging.config.fileConfig('logging.conf')
        return logging.getLogger('sbtGenerator')
