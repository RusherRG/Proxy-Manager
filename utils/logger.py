import logging
import colorlog
import logstash

LOG_LEVEL = logging.INFO


def get_logger(name):

    bold_seq = '\033[1m'
    colorlog_format = (
        f'{bold_seq}'
        '%(log_color)s'
        '%(asctime)s | %(name)s/%(funcName)s | '
        '%(levelname)s:%(reset)s %(message)s'
    )
    colorlog.basicConfig(format=colorlog_format,
                         level=logging.DEBUG, datefmt='%d/%m/%Y %H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    logger.addHandler(logstash.TCPLogstashHandler(
        'localhost', 7000, version=1))

    return logger
