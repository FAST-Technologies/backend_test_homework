from typing import List


class Board:
    """Класс, который описывает игровое поле."""

    field_size: int = 3

    def __init__(self) -> None:
        """Инициализирует игровое поле как двумерный список."""
        self.board: List[List[str]] = [
            [' ' for _ in range(self.field_size)]  # type: List[str]
            for _ in range(self.field_size)
        ]

    def make_move(self, row: int, col: int, player: str) -> None:
        """Выполняет ход, помещая символ игрока в указанную ячейку.

        Args:
            row (int): Номер строки
            col (int): Номер столбца
            player (str): Символ игрока ('X' или 'O')
        """
        self.board[row][col] = player  # type: str

    def display(self) -> None:
        """Отображает текущее состояние игрового поля в консоли."""
        for row in self.board:  # type: List[str]
            print('|'.join(row))  # type: str
            print('-' * 5)  # type: str

    def is_full_board(self) -> bool:
        """Проверяет, заполнено ли игровое поле.

        Returns:
            bool: True, если поле заполнено, иначе False
        """
        for i in range(self.field_size):  # type: int
            for j in range(self.field_size):  # type: int
                if self.board[i][j] == ' ':  # type: str
                    return False
        return True

    def check_win_win_situation(self, player: str) -> bool:
        """Проверяет, выиграл ли указанный игрок.

        Args:
            player (str): Символ игрока ('X' или 'O')

        Returns:
            bool: True, если игрок выиграл, иначе False
        """
        for i in range(3):  # type: int
            if (all([self.board[i][j] == player for j in range(3)]) or
                    all([self.board[j][i] == player for j in range(3)])):
                return True
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2] == player
            or
            self.board[0][2] == self.board[1][1] == self.board[2][0] == player
        ):
            return True
        return False

    def save_result(self, result: str) -> None:
        """Сохраняет результат игры в файл results.txt.

        Args:
            result (str): Строка с результатом игры
        """
        with open('results.txt', 'a') as file:  # type: TextIO
            file.write(str(result) + '\n')  # type: str

    def __str__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Описание размера игрового поля
        """
        return (
            'Объект игрового поля размером '
            f'{self.field_size}x{self.field_size}'  # type: str
        )
