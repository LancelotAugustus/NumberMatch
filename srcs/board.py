class Board:
    """棋盘类"""

    def __init__(self):
        """初始化棋盘"""
        self.digit_list = []

    def __str__(self):
        """可视化棋盘"""
        digit_grid = [self.digit_list[i: i + 9] for i in range(0, len(self.digit_list), 9)]
        return "\n".join(" ".join(str(digit) if digit != 0 else "." for digit in row) for row in digit_grid)

    def set_digits(self, digit_list: list[int]) -> None:
        """
        设置局面

        Args:
            digit_list: 表示局面的整数列表，使用0表示空格
        """
        self.digit_list = digit_list

    def _can_match(self, global_index1: int, global_index2: int) -> bool:
        """
        是否能够配对

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）

        Returns:
            can_match: 如果能够配对则返回True，否则返回False
        """
        digit1 = self.digit_list[global_index1]
        digit2 = self.digit_list[global_index2]
        return digit1 == digit2 or digit1 + digit2 == 10

    def _is_matching(self, global_index1: int, global_index2: int) -> bool:
        """
        是否能够配对消除

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）

        Returns:
            is_matching: 如果能够配对消除则返回True，否则返回False
        """
        if not self._can_match(global_index1, global_index2):
            return False

        if global_index1 == global_index2:
            return False

        digit1 = self.digit_list[global_index1]
        digit2 = self.digit_list[global_index2]

        if digit1 == 0 or digit2 == 0:
            return False

        row_index1, col_index1 = divmod(global_index1, 9)
        row_index2, col_index2 = divmod(global_index1, 9)

        # 相同行
        if row_index1 == row_index2:
            for col_index in range(min(col_index1, col_index2) + 1, max(col_index1, col_index2)):
                if self.digit_list[9 * row_index1 + col_index]:
                    return False
            return True

        # 相同列
        elif col_index1 == col_index2:
            for row_index in range(min(row_index1, row_index2) + 1, max(row_index1, row_index2)):
                if self.digit_list[9 * row_index + col_index1]:
                    return False
            return True

        # 对角线
        elif (row_index1 + col_index1 == row_index2 + col_index2 or
              row_index1 - row_index2 == col_index1 - col_index2):
            row_step = 1 if row_index2 > row_index1 else -1
            col_step = 1 if col_index2 > col_index1 else -1
            for row_index, col_index in zip(range(row_index1 + row_step, row_index2, row_step),
                                            range(col_index1 + col_step, col_index2, col_step)):
                if self.digit_list[9 * row_index + col_index]:
                    return False
            return True

        # 跨行首尾
        elif abs(row_index1 - row_index2) == 1:
            for global_index in range(min(global_index1, global_index2) + 1, max(global_index1, global_index2)):
                if self.digit_list[global_index]:
                    return False
            return True

        # 不相关
        else:
            return False

    def _clear(self) -> None:
        """清理空行"""
        digit_grid = [self.digit_list[i: i + 9] for i in range(0, len(self.digit_list), 9)]
        self.digit_list = [digit for row in digit_grid if any(row) for digit in row]

    def fill(self) -> None:
        """拷贝填充"""
        remaining_digits = [digit for digit in self.digit_list if digit]
        self.digit_list += remaining_digits

    def match(self, global_index1: int, global_index2: int) -> None:
        """
        配对消除

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）
        """
        if self._is_matching(global_index1, global_index2):
            self.digit_list[global_index1] = 0
            self.digit_list[global_index2] = 0
            self._clear()
