from __future__ import annotations
import math
import pygame
from inspect import getsource, isfunction, ismethod
from dataclasses import dataclass

from gameparts import Board
from gameparts.exceptions import FieldIndexError, CellOccupiedError


# Константы, определенные как неизменяемый dataclass
@dataclass(frozen=True)
class Config:
    CELL_SIZE: int = 100  # Размер одной ячейки в пикселях
    BOARD_SIZE: int = 3  # Размер игрового поля (3x3)
    WIDTH: int = 300  # Ширина окна (CELL_SIZE * BOARD_SIZE)
    HEIGHT: int = 300  # Высота окна (CELL_SIZE * BOARD_SIZE)
    LINE_WIDTH: int = 15  # Толщина линий сетки
    BG_COLOR: tuple[int, int, int] = (28, 170, 156)  # Цвет фона
    LINE_COLOR: tuple[int, int, int] = (23, 145, 135)  # Цвет линий
    X_COLOR: tuple[int, int, int] = (84, 84, 84)  # Цвет крестиков
    O_COLOR: tuple[int, int, int] = (242, 235, 211)  # Цвет ноликов
    X_WIDTH: int = 15  # Толщина линий крестиков
    O_WIDTH: int = 15  # Толщина линий ноликов
    SPACE: int = 25  # Отступ внутри ячейки (CELL_SIZE // 4)


# Глобальная константа конфигурации
CONFIG = Config()


def draw_lines(screen: pygame.Surface) -> None:
    """Отрисовывает горизонтальные и вертикальные линии на игровом поле.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
    """
    for i in range(1, CONFIG.BOARD_SIZE):  # type: int
        pygame.draw.line(
            screen,
            CONFIG.LINE_COLOR,
            (0, i * CONFIG.CELL_SIZE),
            (CONFIG.WIDTH, i * CONFIG.CELL_SIZE),
            CONFIG.LINE_WIDTH
        )
        pygame.draw.line(
            screen,
            CONFIG.LINE_COLOR,
            (i * CONFIG.CELL_SIZE, 0),
            (i * CONFIG.CELL_SIZE, CONFIG.HEIGHT),
            CONFIG.LINE_WIDTH
        )


def draw_figures(screen: pygame.Surface, board: list[list[str]]) -> None:
    """Отрисовывает крестики и нолики на доске.

    Args:
        screen (pygame.Surface): Поверхность для отрисовки
        board (list[list[str]]): Двумерный список, представляющий игровое поле
    """
    for row in range(CONFIG.BOARD_SIZE):  # type: int
        for col in range(CONFIG.BOARD_SIZE):  # type: int
            if board[row][col] == 'X':
                pygame.draw.line(
                    screen,
                    CONFIG.X_COLOR,
                    (col * CONFIG.CELL_SIZE + CONFIG.SPACE,
                     row * CONFIG.CELL_SIZE + CONFIG.SPACE),
                    (col * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE - CONFIG.SPACE,
                     row * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE - CONFIG.SPACE),
                    CONFIG.X_WIDTH
                )
                pygame.draw.line(
                    screen,
                    CONFIG.X_COLOR,
                    (col * CONFIG.CELL_SIZE + CONFIG.SPACE,
                     row * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE - CONFIG.SPACE),
                    (col * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE - CONFIG.SPACE,
                     row * CONFIG.CELL_SIZE + CONFIG.SPACE),
                    CONFIG.X_WIDTH
                )
            elif board[row][col] == 'O':
                pygame.draw.circle(
                    screen,
                    CONFIG.O_COLOR,
                    (col * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE // 2,
                     row * CONFIG.CELL_SIZE + CONFIG.CELL_SIZE // 2),
                    CONFIG.CELL_SIZE // 2 - CONFIG.SPACE,
                    CONFIG.O_WIDTH
                )


def run_ui_game(board: Board) -> None:
    """Запускает игру с графическим интерфейсом.

    Args:
        board (Board): Объект игрового поля
    """
    pygame.init()
    screen = pygame.display.set_mode((CONFIG.WIDTH,
                                      CONFIG.HEIGHT))  # type: pygame.Surface
    pygame.display.set_caption('Tic-Tac-Toe')
    screen.fill(CONFIG.BG_COLOR)
    draw_lines(screen)

    current_player: str = 'X'
    running: bool = True

    while running:
        for event in pygame.event.get():  # type: pygame.event.Event
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_y = event.pos[0]
                mouse_x = event.pos[1]
                clicked_row = mouse_x // CONFIG.CELL_SIZE  # type: int
                clicked_col = mouse_y // CONFIG.CELL_SIZE  # type: int

                if board.board[clicked_row][clicked_col] == ' ':
                    board.make_move(clicked_row, clicked_col, current_player)

                    if board.check_win_win_situation(current_player):
                        result = f'Победил игрок {current_player}!'
                        print(result)
                        board.save_result(result)
                        running = False
                    elif board.is_full_board():
                        result = 'Дружеская ничья игроков X и O!'
                        print(result)
                        board.save_result(result)
                        running = False
                    current_player = 'O' if current_player == 'X' else 'X'
                    draw_figures(screen, board.board)

        pygame.display.update()
    pygame.quit()


def run_console_game(board: Board) -> None:
    """Запускает игру в консольном режиме.

    Args:
        board (Board): Объект игрового поля
    """
    current_player: str = 'X'
    running: bool = True

    while running:
        board.display()
        print(f'Ход делает {current_player}')
        while True:
            try:
                row = int(input("Enter row number: "))  # type: int
                if row < 0 or row >= board.field_size:
                    raise FieldIndexError
                column = int(input("Enter column number: "))  # type: int
                if column < 0 or column >= board.field_size:
                    raise FieldIndexError
                if board.board[row][column] != ' ':
                    raise CellOccupiedError
            except FieldIndexError:
                print(
                    'Значение должно быть неотрицательным и меньше '
                    f'{board.field_size}.'
                )
                print('Пожалуйста, введите значения для строки и столбца '
                      'заново.')
                continue
            except ValueError:
                print('Буквы вводить нельзя. Только числа.')
                print('Пожалуйста, введите значения для строки и столбца '
                      'заново.')
                continue
            except Exception as e:
                print(f'Возникла ошибка: {e}')
            else:
                break

        board.make_move(row, column, current_player)
        print(f'Ход сделан игроком {current_player}!')
        board.display()

        if board.check_win_win_situation(current_player):
            result = f'Победил игрок {current_player}!'
            print(result)
            board.save_result(result)
            running = False
        elif board.is_full_board():
            result = 'Дружеская ничья игроков X и O!'
            print(result)
            board.save_result(result)
            running = False
        current_player = 'O' if current_player == 'X' else 'X'


def main() -> None:
    """Запускает основную логику игры."""
    game = Board()  # type: Board
    print(math.__doc__)
    print(print.__doc__)
    print(Board.__doc__)
    print(type(game))
    print(type(game) is Board)
    print(isinstance(game, Board))
    print(isinstance(game, str))
    print(game.__class__)
    print(dir(game))
    print(hasattr(game, '__str__'))
    print(game.__class__.__dict__)
    print(getsource(Board))
    print(isfunction(game.display))
    print(ismethod(game.display))

    # Выбор режима игры
    mode: str = input("Выберите режим игры (console/ui): ").lower()
    if mode == 'ui':
        run_ui_game(game)
    elif mode == 'console':
        run_console_game(game)
    else:
        print("Неверный режим. Используйте 'console' или 'ui'.")
        return


if __name__ == '__main__':
    main()
