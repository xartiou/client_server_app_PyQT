"""Утилиты"""
import sys,os
# sys.path.append(os.path.join(os.getcwd(), '..'))
# sys.path.append('../')
import json

from errors import IncorrectDataRecivedError, NonDictInputError
from common.variables import ENCODING, MAX_PACKAGE_LENGTH
from decorators import log


@log
def get_message(sock):
    """
    Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если принято что-то другое отдаёт ошибку значения
    :param sock:
    :return:
    """

    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(MAX_PACKAGE_LENGTH)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataRecivedError
    else:
        raise IncorrectDataRecivedError

@log
def send_message(sock, message):
    '''
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его на сервер
    '''
    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)