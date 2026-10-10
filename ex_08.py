from datetime import datetime


def original_example() -> None:
    """
    Повторение исходного примера на Java.
    """
    datetime_string: str = "2024-05-13 14:30:00"
    datetime_format:str = "%Y-%m-%d %H:%M:%S"

    try:
        date: datetime = datetime.strptime(datetime_string, datetime_format)
        print(f"Date: {date}")
    except ValueError as e:
        print(f"Ошибка парсинга даты {e}")


"""
Основная проблема исходного примера - отстутствие таймзоны.
В результате, если 2 пользователя находятся в разных таймзонах
и первый ввёл дату время, то для второго её значение будет некорректно.
Например, первый ввёл 14 часов, находясь в Москве, второй
пользователь в Тюмени видит 14 часов, а должен 16 часов.
Более того, даже с одной таймзоной будет некорректно 
показываться дата-время, сохранённое до перехода с летнего на зимнее время,
и наоборот. Необходимо добавить таймзону.
"""


from datetime import timezone, timedelta


def fixed_example() -> None:
    """
    Исправленный пример.
    """
    datetime_string: str = "2024-05-13 14:30:00"
    datetime_format:str = "%Y-%m-%d %H:%M:%S"

    try:
        date: datetime = datetime.strptime(datetime_string, datetime_format)
        date_UTC: datetime = date.replace(tzinfo=timezone(timedelta(seconds=0)))
        print(f"Date UTC: {date_UTC}")
    except ValueError as e:
        print(f"Ошибка парсинга даты {e}")


def main():

    original_example()
    # Вывод:
    # Date: 2024-05-13 14:30:00

    fixed_example()
    # Вывод:
    # Date UTC: 2024-05-13 14:30:00+00:00


if __name__ == "__main__":
    main()
