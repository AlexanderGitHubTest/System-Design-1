"""
Задание: реализуйте класс AverageCalculator, который будет считать среднее арифметическое массива чисел. Напишите тесты для данного класса, но всегда помните, что на практике часто случаются ситуации, когда не все возможные случаи или сценарии тестируются, что может привести к потенциальным ошибкам в коде.

(С этим ничего не поделать: по обширной статистике, 50% ошибок не выявляются в коде даже при 100% его покрытии тестами)

- Реализуйте класс AverageCalculator с методом calculateAverage(int[] numbers).
- Напишите JUnit тесты для данного метода.
- Подумайте, как показать, что при неполном покрытии тестами в программе могут остаться ошибки.
"""
"""
Реализовывать буду на python и с проверкой mypy. По этой причине не проверяю в тесте:
- ошибки, когда не тот тип передали;
- выход за int (в Java выход за int актуален, а python ограничен только 
размером памяти компьютера);
- максимальный размер передаваемого списка (не может превышать sys.maxsize), но при превышении
размера списка его передать методу не получится - ошибка возникнет при создании, а не при передаче.
"""


import pytest


class AverageCalculator:

    def calculate_average(self, numbers: list[int]) -> float:
        """
        Вычисляет среднее арифметическое переданного списка целых чисел.
        """
        return sum(numbers) / len (numbers)


class TestAverageCalculator:

    def test_calculate_average_normal(self) -> None:
        """
        Тестируем среднее списка [1, 2, 3, 4, 5] # 3.0
        """
        average_calculator = AverageCalculator()
        testing_list = [1, 2, 3, 4, 5]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(3.0)

    def test_calculate_average_zero(self) -> None:
        """
        Тестируем список из нулей [0, 0, 0, 0, 0] # 0.0
        """
        average_calculator = AverageCalculator()
        testing_list = [0, 0, 0, 0, 0]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(0.0)

    def test_calculate_average_negative(self) -> None:
        """
        Тестируем список из отрицательных значений [-4, -2, -8, -1, -3] # -3.6
        """
        average_calculator = AverageCalculator()
        testing_list = [-4, -2, -8, -1, -3]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(-3.6)

    def test_calculate_average_fractional(self) -> None:
        """
        Тестируем такой список, чтобы дробное среднее получилось [2, 3] # 2.5
        """
        average_calculator = AverageCalculator()
        testing_list = [2, 3]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(2.5)

    def test_calculate_average_positive_negative(self) -> None:
        """
        Тестируем такой список, чтобы были и положительные 
        и отрицательные [-2, 3, -1] # 0.0
        """
        average_calculator = AverageCalculator()
        testing_list = [-2, 3, -1]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(0.0)

    def test_calculate_average_simple_value(self) -> None:
        """
        Тестируем такой список с одним значением [5] # 5.0
        """
        average_calculator = AverageCalculator()
        testing_list = [5]
        assert average_calculator.calculate_average(testing_list) == pytest.approx(5.0)

    def test_calculate_average_empty(self) -> None:
        """
        Тестируем пустой список []
        """
        # Предположим, что тест пустого списка забыли
        # и при пустом списке будет Exception "ZeroDivisionError"
        # Исправлением функции может быть указать 
        # тип аргумента tuple[int, *tuple[int, ...]]
        # Но тогда придётся при вызове передавать уже кортеж, а не список
        ...


def main():
    average_calculator = AverageCalculator()
    testing_list = [2, 3]
    print(f"Среднее значение для списка {testing_list} "
          + f"равно {average_calculator.calculate_average(testing_list)}")


if __name__ == "__main__":
    main()
