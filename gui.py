from tkinter import Tk, messagebox, Frame, Entry, Label, Button, CENTER, END

from chess import Chess, FigureAlreadySettledError, FigureUnderAttackError, FigureAttacksAnotherError, NoSolutionsError
from console import ChessDrawer
from figures import KingHorseFigure


class Menu:
    def __init__(self, master: Tk):
        self.master = master

        # Запрещаем изменять размер главного меню.
        self.master.resizable(False, False)
        # Изменяем название окна.
        self.master.title('Шахматы :: Главное Меню')

        # Определяем аттрибуты для хранения переменных N, L, K соответственно.
        self.board_size = None
        self.needed_figures = None
        self.placed_figures = None

        # Инициализируем все виджеты главного меню.
        self.__init_main_frame()
        self.__init_board_size_entry()
        self.__init_needed_figures_entry()
        self.__init_placed_figures_entry()
        self.__init_start_button()

        self.master.mainloop()

    def __init_main_frame(self) -> None:
        # Создаем главный фрейм и задаём отступ в 10 пикселей от всех краёв.
        self.main_frame = Frame(self.master)
        self.main_frame.grid(padx=10, pady=10)

    def __init_board_size_entry(self) -> None:
        # Размещаем заголовок для поля.
        Label(self.main_frame, text="Размер доски (N)").grid()
        # Создаем и размещаем по центру поле для ввода N, а так же регистрируем функцию для валидации.
        self.board_size_entry = Entry(
            self.main_frame, validate='key',
            validatecommand=(self.main_frame.register(self.__validate_board_size), '%P'),
            justify=CENTER
        )
        self.board_size_entry.grid(row=1)

    def __validate_board_size(self, value: str) -> bool:
        # Разрешаем оставлять поле пустым (нужно для того, чтобы полностью стереть данные из поля).
        if value == '':
            self.board_size = None
            return True

        # Проверяем, состоит ли введеное значение только из цифр, если да,
        # то проверяем, входит ли оно в интервал, указанный в задаче.
        if value.isdigit() and (1 <= int(value) <= 24):
            # Обновляем значение размера доски.
            self.board_size = int(value)

            # Считаем максимальное количество клеток (фигур), которые теоретически могут находится на доске.
            max_figures = self.board_size ** 2

            # Если в другом поле задано K и оно превышает максимальное количество фигур,
            # то заменяем значение в поле на максимальное количество фигур.
            if self.placed_figures and self.placed_figures > max_figures:
                self.placed_figures_entry.delete(0, END)
                self.placed_figures_entry.insert(0, max_figures)
                self.placed_figures = max_figures

            return True

        return False

    def __init_needed_figures_entry(self) -> None:
        # Размещаем заголовок для поля.
        Label(self.main_frame, text="Кол-во требуемых фигур (L)").grid(row=3)
        # Создаем и размещаем по центру поле для ввода L, а так же регистрируем функцию для валидации.
        self.needed_figures_entry = Entry(
            self.main_frame, validate='key',
            validatecommand=(self.main_frame.register(self.__validate_needed_figures), '%P'),
            justify=CENTER
        )
        self.needed_figures_entry.grid(row=4)

    def __validate_needed_figures(self, value: str) -> bool:
        # Разрешаем оставлять поле пустым (нужно для того, чтобы полностью стереть данные из поля).
        if value == '':
            self.needed_figures = None
            return True

        # Проверяем, состоит ли введеное значение только из цифр, если да,
        # то проверяем, чтобы он было больше или равно 0.
        if value.isdigit() and int(value) >= 0:
            self.needed_figures = int(value)
            return True

        return False

    def __init_placed_figures_entry(self) -> None:
        # Размещаем заголовок для поля.
        Label(self.main_frame, text="Кол-во размещённых фигур (К)").grid(row=5)
        # Создаем и размещаем по центру поле для ввода K, а так же регистрируем функцию для валидации.
        self.placed_figures_entry = Entry(
            self.main_frame, validate='key',
            validatecommand=(self.main_frame.register(self.__validate_placed_figures), '%P'),
            justify=CENTER
        )
        self.placed_figures_entry.grid(row=6)

    def __validate_placed_figures(self, value: str) -> bool:
        # Разрешаем оставлять поле пустым (нужно для того, чтобы полностью стереть данные из поля).
        if value == '':
            self.placed_figures = None
            return True

        # Если в поле введен размер доски, то считаем теоретически максимально возможное количество фигур на доске,
        # иначе считаем его равным максимальному размеру доски в квадрате (576).
        if self.board_size:
            max_figures = self.board_size ** 2
        else:
            max_figures = 576

        # Проверяем, состоит ли введеное значение только из цифр, если да,
        # то проверяем, чтобы оно входило в интервал от 0 до максимально возможного
        # количества фигур на доске включительно.
        if value.isdigit() and (0 <= int(value) <= max_figures):
            self.placed_figures = int(value)
            return True

        return False

    def __init_start_button(self) -> None:
        # Размещаем кнопку, запускающую ввод координат фигур.
        self.start_button = Button(self.main_frame, text="Запустить", command=self.__on_start_button_click)
        self.start_button.grid(row=7, pady=(5, 0))

    def __on_start_button_click(self) -> None:
        # Выдаем ошибку, если не все указанные поля заполнены.
        if self.board_size is None or self.needed_figures is None or self.placed_figures is None:
            messagebox.showerror('Ошибка!', 'Необходимо заполнить все поля!')
            return

        # Создаем интерфейс ввода координат.
        Coordinates(self.board_size, self.needed_figures, self.placed_figures, Tk())


class Coordinates:
    def __init__(self, board_size: int, needed_figures: int, placed_figures: int, master: Tk):
        self.master = master

        # Запрещаем изменять размер окна ввода координат.
        self.master.resizable(False, False)
        # Изменяем название окна.
        self.master.title(f'Шахматы :: Ввод Координат :: N={board_size}, L={needed_figures}, K={placed_figures}')

        # Заполняем основные аттрибуты, полученные из главного меню.
        self.board_size = board_size
        self.needed_figures = needed_figures
        self.placed_figures = placed_figures

        # Создаем экземпляр шахматной доски, вторым аргументом указываем фигуру.
        self.chess = Chess(board_size, KingHorseFigure())

        # Если количество фигур, для которых нужно ввести координаты, то сразу показываем шахматную доску,
        # иначе инциализируем все виджеты окна для ввода координат.
        if self.needed_figures == 0:
            self.__on_create_button_click()
        else:
            self.__init_main_frame()
            self.__init_help_label()
            self.__init_placed_figures_entries()
            self.__init_create_button()

        self.master.mainloop()

    def __init_main_frame(self) -> None:
        # Создаем главный фрейм и задаём отступ в 10 пикселей от всех краёв.
        self.main_frame = Frame(self.master)
        self.main_frame.grid(padx=10, pady=10)

    def __init_help_label(self) -> None:
        # Добавляем заголовок для окна.
        Label(self.main_frame, text="Введите координаты:").grid()

    def __init_placed_figures_entries(self) -> None:
        # Иницализируем пустой список для хранения полей ввода координат.
        self.placed_figures_coordinates_entries = []

        # Регистрируем команду, которая будет валидировать значения вводимые в каждое поле.
        validate_command = self.main_frame.register(self.__validate_coordinates_entry)

        # Создаем поля для ввода координат каждой фигуры.
        for index in range(self.placed_figures):
            # Рассчитываем координаты столбца и строки, чтобы
            # корректно отобразить заголовок поля и само поле.
            column = index // 10
            # Нам необходимо с каждой итерацией получать значение, шаг которого будет увеличиваться на 2.
            row = ((index % 10) + 1) * 2

            # Размещаем заголовок для поля.
            Label(self.main_frame, text=f'№{index + 1}').grid(row=row - 1, column=column)
            # Размещаем поля для ввода координат с зарегистрированной функцией валидации.
            coordinates_entry = Entry(
                self.main_frame, validate='key',
                validatecommand=(validate_command, '%P'),
                justify=CENTER
            )
            coordinates_entry.grid(row=row, column=column, padx=2, pady=2)

            # Добавляем размещенное поле в список.
            self.placed_figures_coordinates_entries.append(coordinates_entry)

    def __validate_coordinates_entry(self, value: str) -> bool:
        # Разрешаем оставлять поле пустым (нужно для того, чтобы полностью стереть данные из поля).
        if value == '':
            return True

        # Разбиваем значение поля по пробелу и с помощью фильтрации, убираем
        # пустые значения (они возникают, если между координатами стоит несколько пробелов.
        coordinates = list(filter(None, value.split()))

        # Проверяем, чтобы количество введеных координат не превышало 2.
        if len(coordinates) > 2:
            return False

        # Проходимся по всем координатам и проверяем их.
        for coordinate in coordinates:
            # Проверяем, что координата состоит только из цифр и входит в
            # интвервал от 0 до размера доски.
            if not coordinate.isdigit() or not (0 <= int(coordinate) < self.board_size):
                return False

        return True

    def __init_create_button(self):
        # Размещаем кнопку, которая будет отображать доску с клетками.
        self.create_button = Button(self.main_frame, text="Создать", command=self.__on_create_button_click)
        self.create_button.grid(row=21, sticky='SW', pady=(5, 0))

    def __on_create_button_click(self) -> None:
        # Пересоздаем шахматную доску для дальнейшего заполнения фигурами.
        self.chess.recreate()

        # Проходимся по всем полям ввода и производим проверки.
        for index, entry in enumerate(self.placed_figures_coordinates_entries):
            value = entry.get()
            # Проверяем, чтобы поле было заполнено.
            if not value:
                messagebox.showerror('Ошибка!', f'Заполните координаты фигуры №{index + 1}.')
                return

            # Получаем координаты, аналогично валидации, и выводим ошибку, если
            # их количество не равно 2.
            coordinates = list(map(int, filter(None, value.split())))
            if len(coordinates) != 2:
                messagebox.showerror('Ошибка!', f'Заполните обе координаты фигуры №{index + 1}.')
                return

            # Распаковываем координаты и пытаемся добавить их на шахматную доску,
            # в случае возникновения ошибки - отображаем её.
            x, y = coordinates
            try:
                self.chess.add_figure(x, y)
            except FigureAlreadySettledError:
                messagebox.showerror('Ошибка!', f'На месте фигуры №{index + 1} имеет дублирующиеся координаты.')
                return
            except FigureUnderAttackError:
                messagebox.showerror('Ошибка!', f'Фигура №{index + 1} находится под атакой других фигур.')
                return
            except FigureAttacksAnotherError:
                messagebox.showerror('Ошибка!', f'Фигура №{index + 1} атакует другие фигуры.')
                return

        # Пытаемся получить матрицу, с рассталенными и фигурами, если решение найдено,
        # то создаем доску, если решений нет - отображаем сообщение об ошибке.
        try:
            self.chess.fill_with_figures(self.needed_figures)
            Board(self.chess, Tk())
        except NoSolutionsError:
            messagebox.showerror('Ошибка!', 'Нет решений!')
            return


class Board:
    def __init__(self, chess: Chess, master: Tk):
        self.master = master
        # Запрещаем изменять размер доски.
        self.master.resizable(False, False)
        # Изменяем название окна.
        self.master.title('Шахматы :: Доска')

        # Инициализируем базовые аттрибуты и создаем "рисовальщик".
        self.chess = chess
        self.chess_drawer = ChessDrawer(self.chess)

        # Инициализируем клеточки и кнопку вывода данных.
        self.__init_cells()
        self.__init_output_button()

    def __init_cells(self):
        # Получаем матрицу с решением из экземпляра класса шахмат.
        matrix = self.chess.matrix

        # Проходимся по всем возможным координатам и создаем ячейки.
        for x in range(self.chess.board_size):
            for y in range(self.chess.board_size):
                # Определяем цвет ячейки, исходя из её значения.
                color = {
                    Chess.EMPTY_CELL: None,
                    Chess.FIGURE_CELL: 'green',
                    Chess.PLACED_FIGURE_CELL: 'red',
                    Chess.ATTACK_CELL: 'blue'
                }[matrix[x][y]]

                # Размещаем ячейку с нужным цветом.
                Button(self.master, height=1, width=2, bg=color, state='disabled').grid(row=y, column=x)

    def __init_output_button(self):
        # Размещаем кнопку вывода.
        self.output_button = Button(self.master, text='Вывести', command=self.__on_output_button_click)
        self.output_button.grid(row=self.chess.board_size, column=0, columnspan=self.chess.board_size)

    def __on_output_button_click(self):
        # Выводим доску в консоль.
        self.chess_drawer.draw_board()
        # Записываем координаты в файл.
        self.chess_drawer.write_coordinates()

        # Выводим успешное сообщение.
        messagebox.showinfo('Успешно!', 'Координаты успешно записаны в файл.')


if __name__ == '__main__':
    Menu(Tk())
