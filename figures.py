class Figure:
    """
    Данный класс является интерфейсом для всех типов фигур.
    """

    @staticmethod
    def get_attack_coordinates(x: int, y: int) -> list:
        """
        Данный метод возвращает координаты клеток, которые будут атакованы фигурой, если она находится на клетке x, y.
        :param x: x координата клетки.
        :param y: y координата клетки.
        :return: Список, состоящий из кортежей вида (x, y).
        """
        raise NotImplementedError()


class KingHorseFigure(Figure):
    """
    Данный класс является реализацией фигуры из варианта №1.
    """

    @staticmethod
    def get_attack_coordinates(x, y) -> list:
        # Заполяем координаты (+-1, +-2) и (+-2, +-1).
        coordinates = [
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x - 2, y + 1),
            (x - 2, y - 1)
        ]

        # Заполяем координаты короля (круг).
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                # Пропускаем клетку, на которой находится наша фигура.
                if i == x and j == y:
                    continue

                # Добавляем пару координат в список.
                coordinates.append((i, j))

        # Возвращаем координаты атаки.
        return coordinates
