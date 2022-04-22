"""Декораторы"""
import sys, os
sys.path.append(os.path.join(os.getcwd(), '..'))
import logging
import logs.server_log_config
import logs.client_log_config
import traceback
import inspect

# Метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.
# os.path.split(sys.argv[0])[1]
if sys.argv[0].find('client_side.py') == -1:
    # если не клиент, то сервер
    CURRENT_LOGGER = logging.getLogger('server_side.py')
else:
    # если не сервер, то клиент
    CURRENT_LOGGER = logging.getLogger('client_side.py')


# Реализация в виде функции
def log(function_to_log):
    """Функция-декоратор"""

    def log_saver(*args, **kwargs):
        """Обертка"""
        ret_func = function_to_log(*args, **kwargs)
        CURRENT_LOGGER.debug(f'Была вызвана функция {function_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {function_to_log.__module__}. '
                     f'Вызов из'f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
                     # f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return ret_func

    return log_saver


# Реализация в виде класса
class Log:
    """Класс-декоратор"""

    def __call__(self, function_to_log):
        def log_saver(*args, **kwargs):
            """Обертка"""
            ret_func = function_to_log(*args, **kwargs)
            CURRENT_LOGGER.debug(f'Была вызвана функция {function_to_log.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {function_to_log.__module__}. Вызов из'
                         f' функции {traceback.format_stack()[0].strip().split()[-1]}.')
                         # f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
            return ret_func

        return log_saver
