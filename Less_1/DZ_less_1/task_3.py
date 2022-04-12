'''
3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера
Но в данном случае результат должен быть итоговым по всем ip-адресам,
представленным в табличном формате (использовать модуль tabulate).
Таблица должна состоять из двух колонок и выглядеть примерно так:
Reachable
10.0.0.1
10.0.0.2

Unreachable
10.0.0.3
10.0.0.4
'''
from tabulate import tabulate
from task_2 import host_range_ping


def host_range_ping_tab():
    """
    Табличное отображение результата перебора ip адресов, вернувшихся из функции host_range_ping
    """
    # запрашиваем хосты, проверяем доступность, получаем словарь результатов
    result_dict = host_range_ping()
    print()
    # выводим в табличном виде
    print(tabulate([result_dict], headers='keys', tablefmt="grid", stralign="center"))


if __name__ == "__main__":
    host_range_ping_tab()

'''
Введите первоначальный адрес: yandex.ru
*** Доменное имя: yandex.ru преобразовано в ip-адрес: 5.255.255.55 ***
Сколько адресов проверить?: 10
5.255.255.55 - Узел доступен
5.255.255.56 - Узел недоступен
5.255.255.57 - Узел недоступен
5.255.255.58 - Узел недоступен
5.255.255.59 - Узел недоступен
5.255.255.60 - Узел доступен
5.255.255.61 - Узел недоступен
5.255.255.62 - Узел недоступен
5.255.255.63 - Узел недоступен
5.255.255.64 - Узел недоступен
+------------------+--------------------+
|  Доступные узлы  |  Недоступные узлы  |
+==================+====================+
|   5.255.255.55   |    5.255.255.56    |
|   5.255.255.60   |    5.255.255.57    |
|                  |    5.255.255.58    |
|                  |    5.255.255.59    |
|                  |    5.255.255.61    |
|                  |    5.255.255.62    |
|                  |    5.255.255.63    |
|                  |    5.255.255.64    |
+------------------+--------------------+
Process finished with exit code 0
'''