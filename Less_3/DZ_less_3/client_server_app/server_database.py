import datetime
from sqlite3 import  *
from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, DateTime, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
from common.variables import *

# Класс - серверная база данных
class ServerStorage:
    # Класс - отображение таблицы всех пользователей
        # Экземпляр этого класса - запись в таблице AllUsers
    class AllUsers:
        def __init__(self, username):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.id = None

    # Класс - отображение таблицы активных пользователей:
        # Экземпляр этого класса - запись в таблице ActiveUsers
    class ActiveUsers:
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    # Класс - отображение таблицы истории входов:
        # Экземпляр этого класса - запись в таблице LoginHistory
    class LoginHistory:
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    def __init__(self):
        # Создаем движок БД
        # SERVER_DATABASE - sqlite:///server_base.db3
        # echo=False - отключает вывод на экран sql-запросов
        # pool_recycle - по умолчанию соединение с БД через 8 часов простоя обрывается,
        # чтобы этого не произошло необходимо pool_recycle=7200(пересоединение через каждые 2 часа)
        self.database_engine = create_engine(SERVER_DATABASE, echo=False, pool_recycle=7200)

        # Создаем объект MetaData
        self.metadata = MetaData()

        # Создаем таблицу пользователей
        user_table = Table('Users', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String, unique=True),
                           Column('last_login', DateTime),
                           )

        # Создаем таблицу активных пользователей
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        # Создаем таблицу истории входов
        user_login_history = Table('Login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        # Создаем таблицы
        self.metadata.create_all(self.database_engine)

        # Создаем отображения
        # Связываем класс в ORM с таблицей
        mapper(self.AllUsers, user_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, user_login_history)

        # Создаем сессию
        Session = sessionmaker(bin=self.database_engine)
        self.session = Session()

        # Если в таблице активных юзеров есть записи, то их нужно удалить
        # Когда устанавливаем соединение, очищаем таблицу активных юзеров
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    # Функция выполняющаяся при входе пользователя записывает в базу факт входа
    def user_login(self, username, ip_address, port):
        print(username, ip_address, port)
        # запрос в таблицу пользователей на наличие пользователей с таким же именем
        rez = self.session.query(self.AllUsers).filter_by(name=username)
        # Если такое имя пользователя уже присутствует в табл, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
        # иначе создаем нового пользователя
        else:
            # Создаем экземпляр класса self.AllUsers, через который передаем данные в табл
            user = self.AllUsers(username)
            self.session.add(user)
            # Чтобы создать нового юзера, id которого будет использовано для добавления в табл active_users_table
            self.session.commit()

        # теперь можно создать запись в active_users_table о факте входа.
        # создаем экземпляр класса self.ActiveUsers, через него и передадим данные в табл
        new_active_user = self.ActiveUsers(user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(new_active_user)

        # # создаем экземпляр класса self.LoginHistory, через него и передадим данные в табл
        history = self.LoginHistory(user.id, datetime.datetime.now(),ip_address, port)
        self.session.add(history)

        # обязательно сохраняем изменения
        self.session.commit()

    # Функция, которая фиксирует отключения пользователя
    def user_logout(self, username):
        # запрашиваем покидающего пользователя из таблицы self.AllUsers
        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        # удаляем его из таблицы self.ActiveUsers
        self.session.query(self.AllUsers).filter_by(user=user.id).delete()
        # commit
        self.session.commit()

    # Функция, которая возвращает список известных пользователей со временем их последнего входа
    def users_list(self):
        # Запрос строк таблицы пользователей.
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
    #     Возвращаем список кортежей
        return query.all()

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем кортежи имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

    # Функция, возвращающая историю входов по пользователю или всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по этому имени
        if username:
            query = query.filter(self.AllUsers.name == username)
        # Возвращаем список кортежей
        return query.all()

# Обязательная отладка
if __name__ == '__main__':
    test_db = ServerStorage()
    # Выполняем "подключение" пользователя
    test_db.user_login('client_1', '192.168.1.4', 8080)
    test_db.user_login('client_2', '192.168.1.5', 7777)

    # Выводим список кортежей - активных пользователей
    print(' ---- test_db.active_users_list() ----')
    print(test_db.active_users_list())

    # Выполняем "отключение" пользователя
    test_db.user_logout('client_1')
    # И выводим список активных пользователей
    print(' ---- test_db.active_users_list() after logout client_1 ----')
    print(test_db.active_users_list())

    # Запрашиваем историю входов по пользователю
    print(' ---- test_db.login_history(client_1) ----')
    print(test_db.login_history('client_1'))

    # и выводим список известных пользователей
    print(' ---- test_db.users_list() ----')
    print(test_db.users_list())