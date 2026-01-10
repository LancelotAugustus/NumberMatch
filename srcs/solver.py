import copy
from typing import Tuple, List
from srcs.board import Board
from srcs.twin_board import TwinBoard


class Solver:
    """求解器类"""

    def __init__(self):
        """初始化求解器"""
        self.board = None
        self.path = []

    def set_board(self, board: Board) -> None:
        """
        设置棋盘

        Args:
            board: Board实例
        """
        self.board = TwinBoard(board)

    def solve(self) -> bool:
        """
        是否能够清空棋盘

        Returns:
            solvability: 如果能够清空棋盘则返回True，否则返回False
        """
        while self.board.digit_pairs:
            best_digit_pair = None
            best_potential_num = - 1

            for digit_pair in self.board.digit_pairs:
                simulated_board = copy.deepcopy(self.board)
                simulated_board.match(digit_pair[0], digit_pair[1])
                potential_num = simulated_board.potential_num
                if potential_num > best_potential_num:
                    best_potential_num = potential_num
                    best_digit_pair = digit_pair

            self.path.append(best_digit_pair)
            self.board.match(best_digit_pair[0], best_digit_pair[1])

            if not self.board.digit_list:
                return True

        return False

    def get_solution(self) -> List[Tuple[int, int]]:
        """
        获取最优消除路径

        Returns:
            path: 最优消除路径
        """
        return self.path
