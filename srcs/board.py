from random import randint
from typing import Tuple


class Board:
    """棋盘类"""

    def __init__(self):
        """初始化棋盘"""
        self.digit_list = []
        self.digit_grid = []

    def __str__(self):
        """可视化棋盘"""
        return "\n".join(" ".join(str(digit) if digit != 0 else "." for digit in row) for row in self.digit_grid)

    @staticmethod
    def calc_coord(global_index: int) -> Tuple[int, int]:
        """
        计算坐标

        Args:
            global_index: 全局索引（0-based）

        Returns:
            row_index: 行索引（0-based）
            col_index: 列索引（0-based）
        """
        row_index = global_index // 9
        col_index = global_index % 9
        return row_index, col_index

    def sync_data(self) -> None:
        """同步数据"""
        self.digit_grid = [self.digit_list[i: i + 9] for i in range(0, len(self.digit_list), 9)]

    def set_board(self, digit_list: list[int]) -> None:
        """
        设置局面

        Args:
            digit_list: 表示局面的整数列表，使用0表示空格
        """
        self.digit_list = digit_list
        self.sync_data()

    def generate_board(self, size: int) -> None:
        """
        生成随机局面

        Args:
            size: 棋盘尺寸
        """
        self.digit_list = [randint(1, 9) for _ in range(size)]
        self.sync_data()

    def is_matching(self, global_index1: int, global_index2: int) -> bool:
        """
        是否配对

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）

        Returns:
            is_matching: 如果能够配对消除则返回True，否则返回False
        """
        if global_index1 == global_index2:
            return False

        digit1 = self.digit_list[global_index1]
        digit2 = self.digit_list[global_index2]

        if digit1 == 0 or digit2 == 0:
            return False

        row_index1, col_index1 = self.calc_coord(global_index1)
        row_index2, col_index2 = self.calc_coord(global_index2)

        if digit1 == digit2 or digit1 + digit2 == 10:
            # 相同行
            if row_index1 == row_index2:
                for col_index in range(min(col_index1, col_index2) + 1, max(col_index1, col_index2)):
                    if self.digit_grid[row_index1][col_index]:
                        return False
                return True

            # 相同列
            elif col_index1 == col_index2:
                for row_index in range(min(row_index1, row_index2) + 1, max(row_index1, row_index2)):
                    if self.digit_grid[row_index][col_index1]:
                        return False
                return True

            # 对角线
            elif (row_index1 + col_index1 == row_index2 + col_index2 or
                  row_index1 - row_index2 == col_index1 - col_index2):
                row_step = 1 if row_index2 > row_index1 else -1
                col_step = 1 if col_index2 > col_index1 else -1
                for row_index, col_index in zip(range(row_index1 + row_step, row_index2, row_step),
                                    range(col_index1 + col_step, col_index2, col_step)):
                    if self.digit_grid[row_index][col_index]:
                        return False
                return True

            # 跨行首尾
            elif abs(row_index1 - row_index2) == 1:
                for global_index in range(min(global_index1, global_index2) + 1, max(global_index1, global_index2)):
                    if self.digit_list[global_index]:
                        return False
                return True

        return False

    def safe_copy(self) -> 'Board':
        """
        安全拷贝

        Returns:
            new_board: Board实例
        """
        new_board = Board()
        new_board.digit_list = self.digit_list[:]
        new_board.digit_grid = [row[:] for row in self.digit_grid]
        return new_board

    def clear(self) -> None:
        """清理空行"""
        self.digit_list = [digit for row in self.digit_grid if any(row) for digit in row]
        self.sync_data()

    def fill(self) -> None:
        """拷贝填充"""
        remaining_digits = [digit for digit in self.digit_list if digit]
        self.digit_list += remaining_digits
        self.sync_data()

    def match(self, global_index1: int, global_index2: int) -> None:
        """配对消除"""
        if self.is_matching(global_index1, global_index2):
            row_index1, col_index1 = self.calc_coord(global_index1)
            row_index2, col_index2 = self.calc_coord(global_index2)
            self.digit_grid[row_index1][col_index1] = 0
            self.digit_grid[row_index2][col_index2] = 0
            self.digit_list[global_index1] = 0
            self.digit_list[global_index2] = 0
            self.clear()
