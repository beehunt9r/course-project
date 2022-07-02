from copy import deepcopy

from figures import Figure


class FigureAttacksAnotherError(RuntimeError):
    """
    Данное исключение необходимо выбрасывать, когда фигура атакует другую фигуру.
    """
    pass


class FigureUnderAttackError(RuntimeError):
    """
    Данное исключение необходимо выбрасывать, когда фигура попадает под атаку другой фигуры.
    """
    pass


class FigureAlreadySettledError(RuntimeError):
    """
    Данное исключение необходимо выбрасывать, когда фигура уже установлена на указанные координаты.
    """
    pass


class NoSolutionsError(RuntimeError):
    """
    Данное исключение необходимо выбрасывать, когда невозможно расставить требуемое количество фигур.
    """
    pass


class Chess:
    """
    Данный класс отвественен за всю внутренюю логику шахмат, его универсальность позволяет
    использовать любые реализации фигур и отображать выходные данные в любом виде.
    """

    # Клетка фигуры.
    FIGURE_CELL = 1
    # Клетка фигуры, раставленной алгоритмом.
    PLACED_FIGURE_CELL = 2
    # Пустая клетка.
    EMPTY_CELL = 0
    # Клетка атаки.
    ATTACK_CELL = -1

    def __init__(self, board_size: int, figure: Figure) -> None:
        self.board_size = board_size
        self.figure = figure
        self.matrix = None

        # Инициализируем пустую доску.
        self.recreate()

    def recreate(self) -> None:
        """
        Данный метод пересоздаёт (очищает) доску.
        :return:
        """
        self.matrix = [[self.EMPTY_CELL for _ in range(self.board_size)] for _ in range(self.board_size)]

    def add_figure(self, x: int, y: int) -> None:
        """
        Данный метод добавляет фигуру на координатную доску и выбрасывает исключение, если добавление невозможно.
        :param x: x координата фигуры.
        :param y: y координата фигуры.
        :return:
        """

        # Если на указанных координатах уже расположена фигура, то выбрасываем исключение.
        if self.matrix[x][y] == self.FIGURE_CELL or self.matrix[x][y] == self.PLACED_FIGURE_CELL:
            raise FigureAlreadySettledError()
        # Если указанные координаты ведут на атаку какой-либо фигуры, то выбрасываем исключение.
        elif self.matrix[x][y] == self.ATTACK_CELL:
            raise FigureUnderAttackError()

        # Генерируем и фильтруем координаты атак фигуры.
        attack_coordinates = self.filter_coordinates(
            self.figure.get_attack_coordinates(x, y)
        )

        # Если фигура атакует какую-либо другую, то выбрасываем исключение.
        if self.__is_figures_under_attack(attack_coordinates):
            raise FigureAttacksAnotherError()

        # На данном этапе все проверки пройдены и мы помечаем клетку фигурой.
        self.matrix[x][y] = self.FIGURE_CELL
        # Так же помечаем все координаты атаки как клетки атаки.
        for coordinates_pair in attack_coordinates:
            x, y = coordinates_pair
            self.matrix[x][y] = self.ATTACK_CELL

    def fill_with_figures(self, count: int) -> bool:
        """
        Данный метод заполняет доску нужным количеством фигур, или выбрасывает исключение если решение невозможно.
        :param count: Количество требуемых фигур.
        :return: Возвращает True, в случае нахождения решения.
        """

        # Скопируем доску, чтобы можно было вернуть изменения в случае ненахождения решения.
        copied_board = deepcopy(self.matrix)

        # Создаем счетчик для подсчета количества расставленных нами фигур.
        figures_counter = 0

        # Перебираем все координаты доски.
        for x in range(self.board_size):
            for y in range(self.board_size):
                # Если требуемое количество координат совпадает с количеством расставленых, завершаем выполнение
                # функции возвращаем True.
                if figures_counter == count:
                    return True

                try:
                    # Пытаемся добавить фигуру на доску.
                    self.add_figure(x, y)
                    # Помечаем, что добавленная фигура является результатом работы алгоритма.
                    self.matrix[x][y] = self.PLACED_FIGURE_CELL

                    # Увеличиваем количество добавленных фигур на 1.
                    figures_counter += 1
                # Если возникла ошибка при расстановке фигуры, то игнорируем её.
                except (FigureAlreadySettledError, FigureUnderAttackError, FigureAttacksAnotherError):
                    pass

        # На данном этапе не удалось расставить требуемое количество фигур,
        # возвращаем доску в исходное состояние и выбрасываем исключение.
        self.board_size = copied_board
        raise NoSolutionsError()

    def get_all_figures(self) -> list:
        """
        Данный метод возвращает список координат фигур, раставленных на доске.
        :return: Список координат, состоящий из кортежей вида (x, y).
        """

        # Создаём пустой список для записи координат.
        coordinates = []

        # Перебираем все координаты доски.
        for x in range(self.board_size):
            for y in range(self.board_size):
                # Если на указанных координатах находится фигура, то записываем данные координаты в список.
                if self.matrix[x][y] == self.FIGURE_CELL or self.matrix[x][y] == self.PLACED_FIGURE_CELL:
                    coordinates.append((x, y))

        # Возвращаем полученные координаты.
        return coordinates

    def __is_figures_under_attack(self, coordinates: list) -> bool:
        """
        Данный метод проверяет, есть ли в списке координаты, которые указывают на фигуру.
        :param coordinates: Список координат, состоящий из кортежей вида (x, y).
        :return:
        """

        # Перебираем все пары координат.
        for coordinates_pair in coordinates:
            # Распаковываем координаты в x и y соотвественно.
            x, y = coordinates_pair

            # Проверяем, есть ли фигура на указанных координатах.
            if self.matrix[x][y] == self.FIGURE_CELL or self.matrix[x][y] == self.PLACED_FIGURE_CELL:
                return True

        return False

    def filter_coordinates(self, coordinates: list) -> list:
        """
        Данный метод отсеивает координаты, выходящие за рамки доски.
        :param self:
        :param coordinates: Список координат, состоящий из кортежей вида (x, y).
        :return: Список координат, состоящий из кортежей вида (x, y).
        """

        return list(
            filter(
                lambda pair: (0 <= pair[0] < self.board_size) and (0 <= pair[1] < self.board_size),
                coordinates
            )
        )


class ChessDrawer:
    """
    Данный класс отвечает за вывод шахматной доски в консоль и за вывод координат всех фигур в файл.
    """

    def __init__(self, chess: Chess) -> None:
        self.chess = chess

    def draw_board(self) -> None:
        """
        Данный метод выводит шахматную доску на консоль, используя символы 0, #, *.
        :return
        """

        # Получаем шахматную доску.
        matrix = self.chess.matrix

        # Перебираем всю шахматную доску.
        for y in range(len(matrix)):
            # Создаем пустой список для символов одной строки.
            symbols = []
            for x in range(len(matrix)):
                # Определяем символ в соотвествии с типом клетки.
                symbol = {
                    Chess.EMPTY_CELL: '0',
                    Chess.ATTACK_CELL: '*',
                    Chess.FIGURE_CELL: '#',
                    Chess.PLACED_FIGURE_CELL: '#'
                }[matrix[x][y]]

                # Добавляем символ в список.
                symbols.append(symbol)

            # Выводим строку в консоль.
            print(' '.join(symbols))

    def write_coordinates(self, file_name: str = 'output.txt') -> None:
        """
        Данный метод записывает координаты всех фигур в указанный файл.
        :param file_name: Название файла, по умолчанию output.txt
        :return:
        """

        # Получаем координаты всех фигур.
        figures_coordinates = self.chess.get_all_figures()

        # Открываем файл для записи.
        file = open(file_name, 'w')
        # В первую строку записываем суммарное количество фигур.
        print(len(figures_coordinates), file=file)
        # Перебираем все пары координат.
        for coordinates_pair in figures_coordinates:
            # Распаковываем координаты в x и y соотвественно.
            x, y = coordinates_pair
            # Записываем строку с координатами.
            print(f'({x}, {y})', file=file)

        # Закрываем файл.
        file.close()

    @staticmethod
    def write_no_solutions(file_name='output.txt') -> None:
        """
        Данный метод no solutions в файл.
        :param file_name: Название файла, по умолчанию output.txt
        :return:
        """
        print('no solutions', file=open(file_name, 'w'))
