from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, override
import re

import openpyxl


class ExcelStorage(ABC):
    """
    Класс предназначен для чтения из файла Excel данных или записи в файл Excel данных.
    Потомки будут реализовывать файлы конкретных форматов. Подразумевается,
    что файл состоит из одного листа, как котором только таблица. Первая строка - заголовки.
    Сам подход ближе всего к паттерну Template.
    """
    def __init__(self, column_headers_correspondence: tuple[tuple[str, str]], filepath: Path) -> None:
        """
        В конструкторе получаем список полей и путь к файлу.
        Список полей состоит из кортежей с двумя полями:
        - первое поле - название столбца в файле
        - второе поле - название поля в словаре в
          списке, который возвращает метод load.
        """
        self._column_headers_correspondence: tuple[tuple[str, str]] = column_headers_correspondence
        self._filepath: Path = filepath

    def load(self) -> list[dict[str, Any]]:
        """
        Загрузка данных из файла. На выходе список 
        словарей с данными (один словарь - одна строка).
        """
        wb: openpyxl.Workbook = openpyxl.load_workbook(
            filename = self._filepath,
            read_only=True,
            data_only=True,
            keep_links=False
        )
        ws = wb.active

        header_row: list[str] = [cell.value for cell in ws[1]]
        expected_headers: list[str] = self.get_column_headers_for_file()
        if header_row != expected_headers:
            raise ValueError(f"Ожидались названия колонок {expected_headers}, найдены {header_row}")

        internal_headers: list[str] = self.get_column_headers_for_internal_use()
        rows: list[dict[str, Any]] = []
        for row_cells in ws.iter_rows(min_row=2, values_only=True):
            row: dict[str, Any] = dict(zip(internal_headers, row_cells))
            self.validate_row(row)
            rows.append(row)

        return rows

    def save(self, rows: list[dict[str, Any]]) -> None:
        """
        Сохранение переданного словаря в файл.
        """
        wb: openpyxl.Workbook = openpyxl.Workbook()
        ws: openpyxl.Worksheet = wb.active
        file_headings: list[str] = self.get_column_headers_for_file()
        ws.append(file_headings)
        internal_headers: list[str] = self.get_column_headers_for_internal_use()        
        for row in rows:
            self.validate_row(row)
            file_row: list[str] = []
            for column_name in internal_headers:
                file_row.append(row[column_name])
            ws.append(file_row)
        wb.save(self._filepath)

    @abstractmethod
    def validate_row(self, row: dict[str, Any]) -> bool:
        """
        Проверка обязательности и корректности данных.
        Метод вызывается для каждой считанной из файла строки.
        """
        ...

    def get_column_headers_for_internal_use(self) -> list[str]:
        """
        Возвращает список заголовков в словаре,
        который возвращает метод load
        """
        return [correspondence[1] for correspondence in self._column_headers_correspondence]

    def get_column_headers_for_file(self) -> list[str]:
        """
        Возвращает список полей, которые
        должны быть заголовками строк в файле.
        """
        return [correspondence[0] for correspondence in self._column_headers_correspondence]



class MontlyBill(ExcelStorage):
    """
    Реализация файла ежемесячного счета.
    """

    def __init__(self, filepath: Path) -> None:
        column_headers_correspondence: tuple[tuple[str, str], ...] = (
            ("Телефонный номер", "phone_number"),
            ("Период начислений", "period"),
            ("Сумма", "summa")
        )
        super().__init__(column_headers_correspondence, filepath)

    @override
    def validate_row(self, row: dict[str, Any]) -> bool:
        """
        Проверка обязательности и корректности данных.
        Метод вызывается для каждой считанной из файла строки.
        """
        # Телефонный номер должен состоять из 10 цифр
        if not re.compile(r"\d{10}").fullmatch(row["phone_number"]):
            raise ValueError(f"Поле 'Телефонный номер' должно состоять" 
                             + f" ровно из 10 цифр, а получено {row["phone_number"]}")
        return True


class MontlyBillReport(ExcelStorage):
    """
    Реализация файла отчета по ежемесячному счету.
    """

    def __init__(self, filepath: Path) -> None:
        column_headers_correspondence: tuple[tuple[str, str], ...] = (
            ("Количество номеров", "phone_number_count"),
            ("Итоговая сумма", "result_summa")
        )
        super().__init__(column_headers_correspondence, filepath)

    @override
    def validate_row(self, row: dict[str, Any]) -> bool:
        """
        Проверка обязательности и корректности данных.
        Метод вызывается для каждой считанной из файла строки.
        """
        # Количество номеров должно быть неотрицательным
        if row["phone_number_count"] < 0:
            raise ValueError(f"Поле 'Количество номеров' должно быть"
                             + f" неотрицательным, а получено {row["phone_number_count"]}")
        return True


def main() -> None:
    """
    Пример использования.
    """
    PATH_BILL: str = "data\\bill2606.xlsx"
    PATH_REPORT: Path = "data\\report2606.xlsx"
    bill: Path = MontlyBill(PATH_BILL).load()
    phone_numbers_count: int = len({row["phone_number"] for row in bill})
    result_summa: float = sum([row["summa"] for row in bill])
    bill_report: list[dict[str, Any]] = [{
        "phone_number_count": phone_numbers_count,
        "result_summa": result_summa
    }]
    MontlyBillReport(PATH_REPORT).save(bill_report)


if __name__ == "__main__":
    main()
