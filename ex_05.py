"""
Имеется класс GradeCalculator с методом calculateAverage(List grades), который вычисляет среднее значение оценок студентов.
Реализуйте этот класс с учётом того, что существуют граничные случаи, которые необходимо правильно обработать, чтобы избежать логических ошибок.
Сделайте пять концептуально различающихся тестов для метода calculateAverage.
"""
"""
Реализовывать буду на python и с проверкой mypy. По этой причине не проверяю в тесте:
- выход за int (в Java выход за int актуален, а python ограничен только 
размером памяти компьютера);
- максимальный размер передаваемого списка (не может превышать sys.maxsize), но при превышении
размера списка его передать методу не получится - ошибка возникнет при создании, а не при передаче.
"""

import datetime
import random
from typing import Literal

import pytest

# Оценки могут быть только 1, 2, 3, 4, 5
GradeValue = Literal[1, 2, 3, 4, 5]


class GradeCalculator:

    def calculate_average(self, numbers: list[GradeValue]) -> float:
        """
        Вычисляет среднее арифметическое переданного списка оценок.
        """
        # Проверка через mypy, assert на случай запуска кода без проверки.
        assert all(numbers) in {1, 2, 3, 4, 5}, "Оценка может быть только 1, 2, 3, 4, 5!"
        # assert на случай пустого списка.
        assert len(numbers) > 0, "Для пустого списка оценок значение среднего не существует!" 
        return sum(numbers) / len (numbers)


class TestGradeCalculator:

    # 1-й тест "happy path".
    # Проверяем работу при правильных данных.
    def test_calculate_average_happy_path(self) -> None:
        """
        Тестируем среднее списка [1, 2, 3, 4, 5] # 3.0
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = [1, 2, 3, 4, 5]
        assert grade_calculator.calculate_average(testing_list) == pytest.approx(3.0)

    # 2-й тест "boundary testing". Корректные, но граничные значения.
    # 1-я часть - список из одного элемента
    def test_calculate_average_single_element(self) -> None:
        """
        Тестируем среднее для списка из одного элемента [3] # 3.0
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = [3]
        assert grade_calculator.calculate_average(testing_list) == pytest.approx(3.0)
    # 2-я часть - огромный список из 1000000 элементов (предположим, что на практике
    # нужны списки меньших значений)
    def test_calculate_average_huge_list(self) -> None:
        """
        Тестируем среднее для списка из миллиона одинаковых элементов [3]*1000000 # 3.0
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = [3]*1000000
        assert grade_calculator.calculate_average(testing_list) == pytest.approx(3.0)

    # 3-й тест "negative testing". Некорректные входные данные.
    # 1-я часть - "переданные числа являются оценками".
    # Проверяем, что будут отслежены ситуации неверных типов данных внутри списка.
    def test_calculate_average_not_grade_values(self) -> None:
        """
        Тестируем список с некорректным значением 0 [1, 2, 0, 4, 5] # AssertionError
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = [1, 2, 0, 4, 5]
        with pytest.raises(AssertionError):
            grade_calculator.calculate_average(testing_list)
    # 2-я часть - "для пустого списка нельзя подсчитывать среднее".
    # Проверяем, что будут отслежены ситуации некорректных вариантов самого списка.
    def test_calculate_average_empty_list(self) -> None:
        """
        Тестируем пустой список [] # AssertionError
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = []
        with pytest.raises(AssertionError):
            grade_calculator.calculate_average(testing_list)

    # 4-й тест "perfomance testing". Проверка производительности.
    # Проверяем, отработает ли список из 10 млн оценок за менее чем секунду
    def test_calculate_average_perfomance(self) -> None:
        """
        Тестируем среднее списка из 10 млн случайных элементов
        Результат не важен, нужно уложиться в 1 секунду. 
        """
        grade_calculator = GradeCalculator()
        testing_list: list[GradeValue] = []
        grade_list: list[GradeValue] = [1, 2, 3, 4, 5]
        for _ in range(10000000):
            testing_list.append(random.choice(grade_list))
        time_begin = datetime.datetime.now()
        grade_calculator.calculate_average(testing_list)
        time_end = datetime.datetime.now()
        assert time_end - time_begin < datetime.timedelta(seconds=1)

    # 5-й тест "white-box testing". Тестирование, зная внутреннее устройство.
    # Для python не применимо, а для Java нужно было бы проверить, что
    # внутри функции нет переполнения (проверить можно, например, передав
    # список из максимальных для int значений).
