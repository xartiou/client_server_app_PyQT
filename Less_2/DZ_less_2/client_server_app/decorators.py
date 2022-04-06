import sys
import traceback
import logging
from logs import client_log_config, server_log_config

if sys.argv[0].find('server.py') == -1:
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func_to_log):
    def log_saver(*args , **kwargs):
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args} , {kwargs}. Вызов из модуля {func_to_log.__module__}')
        ret = func_to_log(*args , **kwargs)
        return ret
    return log_saver