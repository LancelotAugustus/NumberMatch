"""
src/board.py
"""

from random import randint
from typing import Tuple


class Board:
    """棋盘类"""

    def __init__(self):
        """初始化棋盘"""
        self.size = 0
        self.grid = []

    def __str__(self):
        """可视化棋盘"""
        result = []
        for i in range(len(self.grid)):
            row_str = []
            for j in range(len(self.grid[i])):
                digit = self.grid[i][j]
                row_str.append(str(digit) if digit != 0 else ".")
            result.append(" ".join(row_str))
        return "\n".join(result)

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

    def set_grid(self, digit_list: list[int]) -> None:
        """
        设置局面

        Args:
            digit_list: 表示局面的整数列表，使用0表示空格
        """
        self.size = len(digit_list)
        for i in range(self.size):
            if i % 9 == 0:
                self.grid.append([])
                self.grid[-1].append(digit_list[i])
            else:
                self.grid[-1].append(digit_list[i])

    def generate_grid(self, size: int) -> None:
        """
        生成随机局面

        Args:
            size: 棋盘尺寸
        """
        digit_list = [randint(0, 9) for _ in range(size)]
        self.set_grid(digit_list)

    def get_digit_by_coord(self, row_index: int, col_index: int) -> int:
        """
        按坐标获取数字

        Args:
            row_index: 行索引（0-based）
            col_index: 列索引（0-based）

        Returns:
            digit: 指定位置的数字
        """
        digit = self.grid[row_index][col_index]
        return digit

    def get_digit_by_index(self, global_index: int) -> int:
        """
        按坐标获取数字

        Args:
            global_index: 全局索引（0-based）

        Returns:
            digit: 指定位置的数字
        """
        row_index, col_index = self.calc_coord(global_index)
        digit = self.get_digit_by_coord(row_index, col_index)
        return digit

    def set_digit_by_coord(self, row_index: int, col_index: int, digit: int) -> None:
        """
        在指定位置放置数字

        Args:
            row_index: 行索引（0-based）
            col_index: 列索引（0-based）
            digit: 要放置的数字
        """
        self.grid[row_index][col_index] = digit

    def set_digit_by_index(self, global_index: int, digit: int) -> None:
        """
        在指定位置放置数字

        Args:
            global_index: 全局索引（0-based）
            digit: 要放置的数字
        """
        row_index, col_index = self.calc_coord(global_index)
        self.set_digit_by_coord(row_index, col_index, digit)

    def is_matching(self, global_index1: int, global_index2: int) -> bool:
        """
        是否能够配对消除

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）

        Returns:
            is_matching: 如果能够配对消除则返回True，否则返回False
        """
        digit1 = self.get_digit_by_index(global_index1)
        digit2 = self.get_digit_by_index(global_index2)
        row_index1, col_index1 = self.calc_coord(digit1)
        row_index2, col_index2 = self.calc_coord(digit2)

        if global_index1 == global_index2:
            return False
        if digit1 == 0 or digit2 == 0:
            return False

        if digit1 == digit2 or digit1 + digit2 == 10:
            # 相同行
            if row_index1 == row_index2:
                for col_index in range(min(col_index1, col_index2) + 1, max(col_index1, col_index2)):
                    if self.get_digit_by_coord(row_index1, col_index) != 0:
                        return False
                return True

            # 相同列
            elif col_index1 == col_index2:
                for row_index in range(min(row_index1, row_index2) + 1, max(row_index1, row_index2)):
                    if self.get_digit_by_coord(row_index, col_index1) != 0:
                        return False
                return True

            # 对角线
            elif (row_index1 + col_index1 == row_index2 + col_index2 or
                  row_index1 - row_index2 == col_index1 - col_index2):
                row_step = 1 if row_index2 > row_index1 else -1
                col_step = 1 if col_index2 > col_index1 else -1
                row_index, col_index = row_index1 + row_step, col_index1 + col_step
                while row_index != row_index2 and col_index != col_index2:
                    if self.get_digit_by_coord(row_index, col_index) != 0:
                        return False
                    row_index += row_step
                    col_index += col_step
                return True

            # 跨行首尾
            elif abs(row_index1 - row_index2) == 1:
                for global_index in range(min(global_index1, global_index2) + 1, max(global_index1, global_index2)):
                    if self.get_digit_by_index(global_index) != 0:
                        return False
                return True

        return False

    def find_digit_pair(self) -> list[tuple[int, int]]:
        """
        寻找合规数字对

        Returns:
            digit_pair_list: 合规数字对列表
        """
        result = []
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.is_matching(i, j):
                    result.append((i, j))
        return result

    def get_remaining_digits(self) -> list[int]:
        """
        获取剩余数字列表

        Returns:
            remaining_digits: 剩余数字列表
        """
        remaining_digits = []
        for i in range(self.size):
            if digit := self.get_digit_by_index(i):
                remaining_digits.append(digit)
        return remaining_digits

    def get_remaining_digits_num(self) -> int:
        """
        获取剩余数字数量

        Returns:
            remaining_digits: 剩余数字数量
        """
        remaining_digits_num = len(self.get_remaining_digits())
        return remaining_digits_num

    def get_remaining_rows_num(self) -> int:
        """
        获取剩余有效行数量

        Returns:
            remaining_digits: 剩余有效行数量
        """
        remaining_rows_num = len(self.grid)
        return remaining_rows_num

    def safe_copy(self) -> 'Board':
        """
        创建当前棋盘的深拷贝

        Returns:
            new_board: Board实例
        """
        digit_list = []
        for row in self.grid:
            for digit in self.grid[row]:
                digit_list.append(digit)

        new_board = Board()
        new_board.set_grid(digit_list)
        return new_board

    def clear(self) -> None:
        """棋盘操作（被动） —— 清理空行"""
        new_board = []
        for row in self.grid:
            if sum(row) != 0:
                new_board.append(row)
            else:
                self.size -= len(row)
        self.grid = new_board

    def fill(self) -> None:
        """棋盘操作（主动） —— 拷贝填充"""
        replica = self.get_remaining_digits()
        self.size += len(replica)
        filled_digits = [replica[i] for i in range(9 - len(self.grid[-1]))]
        added_digits = [replica[i] for i in range(9 - len(self.grid[-1]), len(replica))]
        for digit in filled_digits:
            self.grid[-1].append(digit)
        for i in range(len(added_digits)):
            if i % 9 == 0:
                self.grid.append([])
                self.grid[-1].append(added_digits[i])
            else:
                self.grid[-1].append(added_digits[i])

    def match(self, global_index1: int, global_index2: int) -> None:
        """棋盘操作（主动） —— 配对消除"""
        if self.is_matching(global_index1, global_index2):
            self.set_digit_by_index(global_index1, 0)
            self.set_digit_by_index(global_index2, 0)
            self.clear()
