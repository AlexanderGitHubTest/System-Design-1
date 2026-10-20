"""
Для перевода в функциональный вид взят класс TileElements
(набор элементов доски) из игры 3-в-ряд.
"""


import random
import string


class TileElements:
    """
    Исходный вид класса.
    """
    """
    АТД TileElements - набор элементов доски.
    Инварианты:
    - все элементы являются большими английскими буквами (от A до Z);
    - все элементы уникальны;
    - элементов не более 5.
    Команды:
    - Исключить элемент
    -- Предусловие - удаляемый элемент должен быть в списке
    -- Постусловие - переданный элемент удалён из набора
    Запросы:
    - Получить следующий случайный элемент
    -- Предусловие - список не пуст
    -- Возвращает - случайный элемент из списка
    """

    def __init__(self, elements: str) -> None:
        self._elements_list: list[str] = list(elements)
        self._invariants()

    def _invariants(self):
        """Проверка инвариантов""" 
        if not (set(self._elements_list) <= set(string.ascii_uppercase)): 
            # Не выполняется условие, что все элементы из set(self._elements_list) входят в set(string.ascii_uppercase)
            raise ValueError(
                f"TileElements must be a single English letters A-Z, got {self._elements_list}"
            )
        if len(self._elements_list) != len(set(self._elements_list)):
            raise ValueError(
                f"All of TileElements must be unique, got {self._elements_list}"
            )
        if len(self._elements_list) > 5:
            raise ValueError(
                f"Length of TileElements must be not greater than 5, got {self._elements_list}"
            )

    def exclude_element(self, element: str) -> None:
        if element not in self._elements_list:
            raise ValueError(
                f"Element must be one of the list, got {elements}"
            )
        self._elements_list.remove(element)
        self._invariants()

    def update_elements(self, elements: str) -> None:
        # Здесь не проверяем: если elements некорректны, так как 
        # ошибки выявятся при создании нового объекта
        return 
        self._elements_list: list[str] = list(elements)


    def next_element(self) -> str:
        if len(self._elements_list) < 1:
            raise ValueError(
                f"TileElements must be not empty, got {self._elements_list}"
            )
        return random.choice(self._elements_list)


#--------------------------------------------------------------------------------------


from typing import Callable, Final, final, Self, TypeVar


T = TypeVar('T')


def pick_with(choosing_function: Callable[[int], int], from_which_choose: list[T]) -> T:
    """
    Специальная чистая функция 'Выбрать с' - служит чтобы можно было
    вместо 'нечистой' random.randrange при необходимости 
    подставлять чистую mock-функцию для тестирования.
    """
    index: int = choosing_function(len(from_which_choose))
    return from_which_choose[index]


@final
class TileElementsFunctionalStyle:
    """
    Класс в функциональном стиле.
    """
    """
    АТД TileElements - набор элементов доски.
    Инварианты:
    - все элементы являются большими английскими буквами (от A до Z);
    - все элементы уникальны;
    - элементов не более 5.
    Команды:
    - Исключить элемент
    -- Предусловие - удаляемый элемент должен быть в списке
    -- Постусловие - переданный элемент удалён из набора
    Запросы:
    - Получить следующий случайный элемент
    -- Предусловие - список не пуст
    -- Возвращает - случайный элемент из списка
    """

    def __init__(self, elements: str) -> None:
        if not (set(elements) <= set(string.ascii_uppercase)): 
            # Не выполняется условие, что все элементы из set(elements) входят в set(string.ascii_uppercase)
            raise ValueError(
                f"TileElements must be a single English letters A-Z, got {elements}"
            )
        if len(elements) != len(set(elements)):
            raise ValueError(
                f"All of TileElements must be unique, got {elements}"
            )
        if len(elements) > 5:
            raise ValueError(
                f"Length of TileElements must be not greater than 5, got {elements}"
            )
        self._elements_list: Final[list[str]] = list(elements)

    def exclude_element(self, element: str) -> Self:
        if len(element) != 1:
            raise ValueError(
                f"Element must be one letter, got {elements}"
            )
        if element not in self._elements_list:
            raise ValueError(
                f"Element must be one of the list, got {elements}"
            )
        return TileElementsFunctionalStyle("".join(letter for letter in self._elements_list if letter != element))

    def update_elements(self, elements: str) -> Self:
        # Здесь не проверяем: если elements некорректны, так как 
        # ошибки выявятся при создании нового объекта
        return TileElementsFunctionalStyle(elements)

    def next_element(self) -> str:
        if len(self._elements_list) < 1:
            raise ValueError(
                f"TileElements must be not empty, got {self._elements_list}"
            )
        return pick_with(random.randrange, self._elements_list)

    def __str__(self) -> str:
        return "".join(self._elements_list)


#--------------------------------------------------------------------------------------


def main():
    tile_elements: TileElementsFunctionalStyle = TileElementsFunctionalStyle("ABCDE")
    print(f"Tile elements = {str(tile_elements)}") # "Tile elements = ABCDE"

    tile_elements = tile_elements.exclude_element("D")
    print(f"Tile elements = {str(tile_elements)}") # "Tile elements = ABCE"

    tile_elements = tile_elements.update_elements("ASDFG")
    print(f"Tile elements = {str(tile_elements)}") # "Tile elements = ASDFG"

    print(f"Next element = {tile_elements.next_element()}") # "Next element = S" (random choice)


if __name__ == "__main__":
    main()
