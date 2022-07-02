from chess import Chess, NoSolutionsError, ChessDrawer
from figures import KingHorseFigure

# Открываем файл с входными данными.
input_file = open('input.txt', 'r')

# Получаем из консоли и преобразовываем значения N, L и K соотвественно.
board_size, needed_figures, placed_figures = map(int, input_file.readline().strip().split())

# Создаем экземпляр класса шахмат.
chess = Chess(board_size, KingHorseFigure())

# Создаем экземпляр класса-хелпера.
chess_drawer = ChessDrawer(chess)

# Расставляем все фигуры.
for _ in range(placed_figures):
    # Получаем координаты фигуры.
    x, y = map(int, input_file.readline().strip().split())

    # Добавляем фигуру на шахматную доску.
    chess.add_figure(x, y)

try:
    chess.fill_with_figures(needed_figures)
    chess_drawer.write_coordinates()
except NoSolutionsError:
    ChessDrawer.write_no_solutions()

chess_drawer.draw_board()
