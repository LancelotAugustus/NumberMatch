from srcs.board import Board


class TwinBoard(Board):
    """孪生棋盘类"""

    def __init__(self, board: Board):
        """
        初始化孪生棋盘

        Args:
            board: Board实例
        """
        super().__init__()
        self.digit_list = [min(digit, 10 - digit) if digit else 0 for digit in board.digit_list]
        self._analyze()

    def _can_match(self, global_index1: int, global_index2: int) -> bool:
        """
        是否能够配对

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）

        Returns:
            can_match: 如果能够配对则返回True，否则返回False
        """
        return self.digit_list[global_index1] == self.digit_list[global_index2]

    def _analyze(self) -> None:
        """更新信息"""
        self.pair_list = []
        self.score = 0

        for i in range(len(self.digit_list)):
            for j in range(i + 1, len(self.digit_list)):
                if self._can_match(i, j):
                    self.score += 1
                if self._is_pair(i, j):
                    self.pair_list.append((i, j))

    def match(self, global_index1: int, global_index2: int) -> None:
        """
        配对消除

        Args:
            global_index1: 全局索引（0-based）
            global_index2: 全局索引（0-based）
        """
        super().match(global_index1, global_index2)
        self._analyze()
