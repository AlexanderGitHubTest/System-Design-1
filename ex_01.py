from __future__ import annotations


"""
Задание.
Добавьте реализацию Storage с использованием базы данных.
Напишите программу, которая сохраняет несколько строк в хранилище, и затем извлекает их. 
"""
"""
Реализация.
Не стал использовать JDBC или похожий по смыслу ODBC. Причина - всё-равно остаётся проблема диалектов SQL для разных баз.
Поэтому пришлось бы делать реализацию не для баз данных, а для конкретной базы.
Сделал универсальный интерфейс базы данных DataBase, его наследники реализуют уже взаимодействие с конкретной базой данных.
При этом для InDataBaseStorage существует только универсальный Database.
"""


from abc import ABC, abstractmethod
import sqlite3
from typing import override


# DataBase.python
class DataBase(ABC):
    """
    Интерфейс, которые определяет взаимодействие 
    с базой данных
    """
   
    @abstractmethod
    def save_new_data_to_table(self, data: list[str]) -> None:
        ...

    @abstractmethod
    def retrieve_data_from_table(self) -> list[str]:
        ...

    @abstractmethod
    def clear_data_in_table(self) -> None:
        ...


# SQLiteDataBase.python
class SQLiteDataBase(DataBase):
    """
    Реализация взаимодействия с базой данных
    для SQLite
    """

    DATABASE_NAME: str = "default.db"
    TABLE_NAME: str = "item"
    ID_FIELD_NAME: str = "id"
    DATA_FIELD_NAME: str = "data"

    def _create_table(self) -> sqlite.Cursor:
        connection = sqlite3.connect(self.DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                {self.ID_FIELD_NAME} INTEGER PRIMARY KEY AUTOINCREMENT,
                {self.DATA_FIELD_NAME} TEXT
            )
        """)
        return connection, cursor

    @override
    def save_new_data_to_table(self, data: list[str]) -> None:
        connection, cursor = self._create_table()
        cursor.execute(f"""
            DELETE FROM {self.TABLE_NAME}
        """)
        connection.commit()
        for item in data:
            cursor.execute(f"""
                INSERT INTO {self.TABLE_NAME}
                ({self.DATA_FIELD_NAME}) VALUES (?) 
            """, (item,))
        connection.commit()
        connection.close()      
            
    @override
    def retrieve_data_from_table(self) -> list[str]:
        connection, cursor = self._create_table()
        items_from_table = cursor.execute(f"""
            SELECT {self.DATA_FIELD_NAME} FROM {self.TABLE_NAME};
        """)
        result: list[str] = []
        for item in items_from_table.fetchall():
            result.append(item[0])
        connection.close()
        return result

    @override
    def clear_data_in_table(self) -> None:
        connection, cursor = self._create_table()
        cursor.execute(f"""
            DELETE FROM {self.TABLE_NAME}
        """)
        connection.commit()


# Storage.python
class Storage(ABC):
    """
    Интерфейс, который определяет контракт 
    для хранения и получения данных.
    """

    @abstractmethod
    def save(self, data: str) -> None:
        ...

    @abstractmethod
    def retrieve(self, id: int) -> str:
        ...


# InDataBaseStorage.python
class InDataBaseStorage(Storage):
    """
    Реализация интерфейса, сохраняющая данные
    в базе данных.

    Получает объект базы данных для использования
    в качестве постоянной памяти.
    """

    def __init__(self, database: Database) -> None:
        self._database: Database = database
        self._storage: list[str] = database.retrieve_data_from_table()
      
    @override
    def save(self, data: str) -> None:
        self._storage.append(data)
        self._database.save_new_data_to_table(self._storage)

    @override
    def retrieve(self, id: int) -> str:
        return self._storage[id]


def main() -> None:
    # Тестовые строки.
    test_strs = ["test1", "test2", "test3"]
    # Используем SQLite.
    db = SQLiteDataBase()
    # Очищаем базу данных
    db.clear_data_in_table()
    # Создаём объект Storage
    idbs = InDataBaseStorage(db)
    # Сохраняем строки в Storage
    for s in test_strs:
        idbs.save(s)
    # Удаляем объект хранилища
    del(idbs)
    # Удаляем объект связи с базой данных
    del(db)
    # Заново создаём объект связи с SQLite.
    db = SQLiteDataBase()
    # Заново создаём объект хранилища
    idbs = InDataBaseStorage(db)
    # Считываем из Storage строки и сравниваем с исходными
    for i in range(3):
        assert idbs.retrieve(i) == test_strs[i]


if __name__ == "__main__":
    main()
