
# -Исходный вариант -------------------------------------------------------------------

"""
В исходном варианте была проблема, что вся логика поиска
размещалась в методе и так большого класса Board,
а также любое добавление изменялос бы этот метод.
"""


# figures_and_bonuses.py
class Figure:
    """ Одна фигура на поле, это не форма, а конкретная фигура """
    LINE = "line"
    L_SHAPE = "l_shape"

    def __init__(self, kind: str, positions: frozenset[Position]):
        assert len(positions) >= 3          # Фигура больше 3-х элементов
        assert kind in (self.LINE, self.L_SHAPE)  # Поддерживаемые типы фигур
        self.kind = kind
        self.positions = positions

    # Запросы
    @property
    def points(self) -> int:
        # Число очков за фигуру
        table = [10, 40, 200, 1200, 8400, 67200] # Для 3, 4, 5, 6, 7, 8 элементов
        return table[(len(self.positions) - 3)]


# board.py

class Board:

    # ...
    # Прочие методы класса Board не показаны
    # ...

    @staticmethod
    def _find_longest_sequence_regex(board_row:list):
        """
        Находит самую длинную последовательность одинаковых элементов,
        используя регулярные выражения.
        """   
        # Преобразуем список в строку
        board_row_str = "".join(board_row)
        
        # Ищем все последовательности повторяющихся символов
        # (.) - захватываем символ, \1* - повторение того же символа
        matches = list(re.finditer(r"(.)\1*", board_row_str))
   
        # Находим совпадение максимальной длины
        longest = max(matches, key=lambda m: len(m.group()))
    
        return (longest.start(), len(longest.group()))


    def search_figure(self) -> Figure | NoneClass:
        """ Ищет фигуру максимального размера: линии и L-образные """

        candidates: list[tuple[int, int, Figure]] = []

        # --- Горизонтальные последовательности ---
        # Ключ: номер столбца (column), значение: (start_row, length)
        h_figures = {}
        for column in range(self.SIZE):
            h_figures[column] = self._find_longest_sequence_regex(self._grid[column])

        # --- Вертикальные последовательности ---
        # Для вертикали читаем элементы по строке (фиксированный row, меняется column)
        # Ключ: номер строки (row), значение: (start_column, length)
        v_figures = {}
        for row in range(self.SIZE):
            vertical_slice = [self._grid[column][row] for column in range(self.SIZE)]
            v_figures[row] = self._find_longest_sequence_regex(vertical_slice)

        # --- Обработка горизонтальных линий ---
        for col, (start_row, length) in h_figures.items():
            if length < 3:
                continue
            element = self._grid[col][start_row]
            positions = frozenset(
                Position(column=col, row=start_row + i) for i in range(length)
            )
            for end_row in (start_row, start_row + length - 1):
                for dc in (-1, 1):
                    adj_col = col + dc
                    if 0 <= adj_col < self.SIZE and self._grid[adj_col][end_row] == element:
                        l_positions = frozenset(
                            set(positions) | {Position(column=adj_col, row=end_row)}
                        )
                        candidates.append(
                            (len(l_positions), 2, Figure(Figure.L_SHAPE, l_positions))
                        )
            candidates.append((length, 1, Figure(Figure.LINE, positions)))

        # --- Обработка вертикальных линий ---
        for row, (start_col, length) in v_figures.items():
            if length < 3:
                continue
            element = self._grid[start_col][row]
            positions = frozenset(
                Position(column=start_col + i, row=row) for i in range(length)
            )
            for end_col in (start_col, start_col + length - 1):
                for dr in (-1, 1):
                    adj_row = row + dr
                    if 0 <= adj_row < self.SIZE and self._grid[end_col][adj_row] == element:
                        l_positions = frozenset(
                            set(positions) | {Position(column=end_col, row=adj_row)}
                        )
                        candidates.append(
                            (len(l_positions), 2, Figure(Figure.L_SHAPE, l_positions))
                        )
            candidates.append((length, 1, Figure(Figure.LINE, positions)))

        if not candidates:
            return void

        best = max(candidates, key=lambda c: (c[0], c[1]))
        return best[2]


# -Изменённый вариант -------------------------------------------------------------------

"""
В измененном варианте поиск фигур выделен в один класс, причем абстрактный,
поиск производится по его потомкам (полиморфизм), а доска передаётся этому классу как
параметр (Dependency Injection).
"""


# figures_and_bonuses.py

@dataclass(frozen=True)
class Run:
    """ Самая длинная последовательность одинаковых элементов в строке или столбце доски """
    element: str
    positions: tuple[Position, ...]
    # Направление, перпендикулярное последовательности: (column, row)
    perpendicular: tuple[int, int]


class FigureFinder(ABC):
    """
    ИскательФигур - абстрактный класс поиска фигур на доске.
    Потомки реализуют поиск конкретного вида фигур в методе find.
    Доска передаётся как grid[column][row].
    """
    # Приоритет вида фигур при равном размере (больше - важнее)
    PRIORITY: int = 0

    @abstractmethod
    def find(self, grid: list[list[str]]) -> list[Figure]:
        """ Возвращает все найденные фигуры своего вида """

    @staticmethod
    def find_longest_sequence_regex(board_row: list) -> tuple[int, int]:
        """
        Находит самую длинную последовательность одинаковых элементов,
        используя регулярные выражения. Возвращает (начало, длина).
        """
        # Преобразуем список в строку
        board_row_str = "".join(board_row)

        # Ищем все последовательности повторяющихся символов
        # (.) - захватываем символ, \1* - повторение того же символа
        matches = list(re.finditer(r"(.)\1*", board_row_str))

        # Находим совпадение максимальной длины
        longest = max(matches, key=lambda m: len(m.group()))

        return (longest.start(), len(longest.group()))

    @classmethod
    def iter_runs(cls, grid: list[list[str]], min_length: int = 3) -> Iterator[Run]:
        """
        Перебирает самые длинные последовательности длиной не менее min_length:
        сначала по каждому столбцу (grid[column]), затем по каждой строке.
        """
        size = len(grid)

        for column in range(size):
            start, length = cls.find_longest_sequence_regex(grid[column])
            if length < min_length:
                continue
            yield Run(
                element=grid[column][start],
                positions=tuple(Position(column=column, row=start + i) for i in range(length)),
                perpendicular=(1, 0),
            )

        for row in range(size):
            vertical_slice = [grid[column][row] for column in range(size)]
            start, length = cls.find_longest_sequence_regex(vertical_slice)
            if length < min_length:
                continue
            yield Run(
                element=vertical_slice[start],
                positions=tuple(Position(column=start + i, row=row) for i in range(length)),
                perpendicular=(0, 1),
            )


class LineFinder(FigureFinder):
    """ Поиск линий """
    PRIORITY = 1

    def find(self, grid: list[list[str]]) -> list[Figure]:
        return [
            Figure(Figure.LINE, frozenset(run.positions))
            for run in self.iter_runs(grid)
        ]


class LShapeFinder(FigureFinder):
    """ Поиск фигур L-типа: линия, к краю которой сбоку примыкает элемент такого же типа"""
    PRIORITY = 2

    def find(self, grid: list[list[str]]) -> list[Figure]:
        size = len(grid)
        figures: list[Figure] = []
        for run in self.iter_runs(grid):
            d_column, d_row = run.perpendicular
            for end in (run.positions[0], run.positions[-1]):
                for sign in (-1, 1):
                    column = end.column + sign * d_column
                    row = end.row + sign * d_row
                    if 0 <= column < size and 0 <= row < size and grid[column][row] == run.element:
                        positions = frozenset(run.positions) | {Position(column=column, row=row)}
                        figures.append(Figure(Figure.L_SHAPE, positions))
        return figures


# board.py

class Board:

    # ...
    # Прочие методы класса Board не показаны
    # ...

    """
    В классе Board сохранился метод, но он теперь только перебирает
    классы для поиска элементов, поэтому при добавлении новых
    фигур данный метод изменяться не будет.
    P.S. Пока получился "своеобразный" поиск - "линия и добавление к ней".
    Скорее всего, это будет переделано, но архитектурное решение по
    вынесению логики поиска в другой класс сохранится.
    """

    def search_figure(self) -> Figure | NoneClass:
        """ Ищет фигуру максимального размера: линии и L-образные """

        candidates: list[tuple[int, int, Figure]] = []

        # Запускаем поиск всеми "искателями" фигур (потомками FigureFinder)
        for finder_class in FigureFinder.__subclasses__():
            finder = finder_class()
            for figure in finder.find(self._grid):
                candidates.append((len(figure.positions), finder.PRIORITY, figure))

        if not candidates:
            return void

        best = max(candidates, key=lambda c: (c[0], c[1]))
        return best[2]
