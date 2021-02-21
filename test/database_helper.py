import mysql.connector
import logging

connection: mysql.connector.Connect


def connect_to_database():
    global connection
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="user",
            password="pass",
            database="flaskini"
        )
    except mysql.connector.Error as err:
        logging.error(err)


def disconnect_from_database():
    connection.close()


def execute(*commands):
    cursor = connection.cursor()
    for command in commands:
        cursor.execute(command)
    connection.commit()
    return cursor


def query(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor


def prepare_database(before, after):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            connect_to_database()
            execute(*before)
            try:
                response = f(*args, **kwargs)
            finally:
                execute(*after)
                disconnect_from_database()
            return response
        return wrapped
    return inner_decorator


def test_clean_database_helper():
    connect_to_database()
    execute('DELETE FROM list;')
    disconnect_from_database()