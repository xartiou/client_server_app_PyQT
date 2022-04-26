"""Константы"""

import logging

# IP-адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Порт по умолчанию для сетевого взаимодействия
DEFAULT_PORT = 8888
# Максимальная очередь подключений
MAX_CONNECTIONS = 1
# Максимальная длина сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи, используемые в протоколе:
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONSE_DEFAULT_IP_ADDRESS = 'response_default_ip_address'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'

# Словари-ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}

