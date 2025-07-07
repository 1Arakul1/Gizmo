# database_utils.py
"""
Скрипт для создания базы данных MS SQL Server.

Этот скрипт предназначен для создания базы данных MS SQL Server, если она не существует.
Он использует параметры подключения, указанные в файле .env.
"""
print ("СТАРТ")
import os
import pyodbc
from dotenv import load_dotenv

def create_database():
    """
    Создает базу данных MS SQL Server, если она не существует.
    
    Считывает параметры подключения из переменных окружения, загруженных из .env файла.
    Проверяет, существует ли база данных с указанным именем, и, если нет, создает ее.
    """
    load_dotenv()

    db_name = os.getenv("DJANGO_DATABASE_NAME", "Gizmo") 
    db_user = os.getenv("DJANGO_DATABASE_USER")
    db_password = os.getenv("DJANGO_DATABASE_PASSWORD")
    db_host = os.getenv("DJANGO_DATABASE_HOST")

    if not all([db_user, db_password, db_host]):
        print("Ошибка: Не все необходимые переменные окружения установлены.")
        return

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host};UID={db_user};PWD={db_password}'
    cnxn = None

    try:
        cnxn = pyodbc.connect(connection_string, autocommit=True)
        cursor = cnxn.cursor()

        # Проверяем, существует ли база данных
        cursor.execute(f"SELECT database_id FROM sys.databases WHERE name = '{db_name}'")
        result = cursor.fetchone()

        if result:
            print(f"База данных '{db_name}' уже существует.")
            return

        # Создаем базу данных
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"База данных '{db_name}' успешно создана.")

    except pyodbc.Error as ex:
        print(f"Ошибка при создании базы данных: {ex}")

    finally:
        if cnxn:
            cnxn.close()

if __name__ == "__main__":
    create_database()