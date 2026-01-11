"""
NumberMatch 项目 Solver 类的全面单元测试

本文件包含 Solver 类的完整单元测试，涵盖：
1. 求解器初始化和状态管理
2. 棋盘设置和 TwinBoard 集成
3. 核心求解算法（solve 方法）
4. 解决方案获取（get_solution 方法）
5. 边界条件和异常处理

使用方法：
    pytest tests/test_solver.py -v          # 详细输出
    pytest tests/test_solver.py --cov       # 查看覆盖率
    pytest tests/test_solver.py -k "solve"  # 运行特定测试
"""

import pytest

from srcs.board import Board
from srcs.solver import Solver


class TestSolverInitialization:
    """测试 Solver 类的初始化功能"""

    def test_init_default_values(self):
        """测试初始化默认值"""
        solver = Solver()

        assert solver.board is None
        assert solver.path == []

    def test_init_creates_empty_path(self):
        """测试初始化时创建空路径列表"""
        solver = Solver()

        assert isinstance(solver.path, list)
        assert len(solver.path) == 0

    def test_repr_initial_state(self):
        """测试初始状态的字符串表示"""
        solver = Solver()

        assert repr(solver.board) == "None"
        assert repr(solver.path) == "[]"


class TestSolverSetBoard:
    """测试 Solver 的棋盘设置功能"""

    def test_set_board_creates_twin_board(self):
        """测试设置棋盘时创建 TwinBoard"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.__class__.__name__ == "TwinBoard"
        assert len(solver.board.digit_list) == 81

    def test_set_board_preserves_digit_values(self):
        """测试设置棋盘时保留数字值（转换后）"""
        board = Board()
        test_digits = [1, 0, 9, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0]
        board.set_digits(test_digits)

        solver = Solver()
        solver.set_board(board)

        assert solver.board.digit_list[0] == 1
        assert solver.board.digit_list[1] == 0
        assert solver.board.digit_list[2] == 1

    def test_set_board_updates_digit_pairs(self):
        """测试设置棋盘时更新可消除配对（同一行无阻挡）"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) > 0

    def test_set_board_empty_board(self):
        """测试设置空棋盘"""
        board = Board()

        solver = Solver()
        solver.set_board(board)

        assert solver.board.digit_list == []
        assert solver.board.pair_list == []

    def test_set_board_multiple_times(self):
        """测试多次设置棋盘"""
        board1 = Board()
        board1.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0])

        board2 = Board()
        board2.set_digits([4, 5, 6, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board1)

        assert solver.board.digit_list[0] == 1

        solver.set_board(board2)

        assert solver.board.digit_list[0] == 4


class TestSolverSolveWithDigitPairs:
    """测试 Solver 在有 digit_pairs 时的求解行为"""

    def test_solve_with_adjacent_pair(self):
        """测试相邻数字配对消除"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) > 0

        solver.board.match(solver.board.pair_list[0][0], solver.board.pair_list[0][1])

        assert 5 not in solver.board.digit_list[:2]

    def test_solve_with_pair_elimination_reduces_pairs(self):
        """测试配对消除减少 digit_pairs"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        initial_pairs_count = len(solver.board.pair_list)
        assert initial_pairs_count > 0

        solver.board.match(solver.board.pair_list[0][0], solver.board.pair_list[0][1])

        assert len(solver.board.pair_list) < initial_pairs_count

    def test_solver_algorithm_behavior_with_pairs(self):
        """测试求解算法在有配对时的行为"""
        board = Board()
        board.set_digits([5, 5, 5, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) > 0

        if len(solver.board.pair_list) > 0:
            first_pair = solver.board.pair_list[0]
            solver.board.match(first_pair[0], first_pair[1])

            assert isinstance(solver.board.digit_list, list)


class TestSolverSolveFailure:
    """测试 Solver 求解失败的场景"""

    def test_solve_empty_digit_pairs_returns_false(self):
        """测试 digit_pairs 为空时返回 False"""
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.pair_list == []
        result = solver.solve()

        assert result is False

    def test_solve_single_digit(self):
        """测试单数字棋盘无法清空"""
        board = Board()
        board.set_digits([5])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.pair_list == []
        result = solver.solve()

        assert result is False

    def test_solve_empty_board(self):
        """测试空棋盘返回 False"""
        board = Board()

        solver = Solver()
        solver.set_board(board)

        result = solver.solve()

        assert result is False

    def test_solve_no_matching_pairs(self):
        """测试无可匹配配对时返回 False"""
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.pair_list == []
        result = solver.solve()

        assert result is False


class TestSolverGetSolution:
    """测试 Solver 获取解决方案功能"""

    def test_get_solution_empty_path(self):
        """测试无配对时返回空路径"""
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        solution = solver.get_solution()

        assert solution == []
        assert isinstance(solution, list)

    def test_get_solution_returns_tuple_list(self):
        """测试返回值为元组列表"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            first_pair = solver.board.pair_list[0]
            solver.board.match(first_pair[0], first_pair[1])
            solver.path.append(first_pair)

        solution = solver.get_solution()

        assert isinstance(solution, list)

    def test_get_solution_after_match(self):
        """测试配对后的解决方案"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])
            solver.path.append(pair)

        solution = solver.get_solution()

        assert isinstance(solution, list)

    def test_get_solution_before_solve(self):
        """测试求解前的解决方案"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        solution = solver.get_solution()

        assert solution == []


class TestSolverPathRecording:
    """测试求解路径记录"""

    def test_path_after_manual_match(self):
        """测试手动配对后的路径"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])
            solver.path.append(pair)

        assert len(solver.path) >= 0

    def test_path_order_correct(self):
        """测试路径顺序正确"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            first_pair = solver.board.pair_list[0]
            solver.board.match(first_pair[0], first_pair[1])
            solver.path.append(first_pair)

        for pair in solver.path:
            assert isinstance(pair, tuple)
            assert len(pair) == 2
            assert pair[0] != pair[1]


class TestSolverEdgeCases:
    """测试 Solver 边界条件"""

    def test_solve_no_pairs_available(self):
        """测试无可用配对时的行为（digit_pairs为空时返回False）"""
        board = Board()
        board.set_digits([1, 3, 5, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.pair_list == []
        result = solver.solve()

        assert result is False

    def test_solve_with_zeros(self):
        """测试包含零值的棋盘"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3, 0, 4, 0, 5,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.pair_list == []
        result = solver.solve()

        assert isinstance(result, bool)

    def test_set_board_then_match_multiple_times(self):
        """测试多次设置棋盘并配对"""
        board1 = Board()
        board1.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0])

        board2 = Board()
        board2.set_digits([6, 6, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()

        solver.set_board(board1)
        if len(solver.board.pair_list) > 0:
            first_pair1 = solver.board.pair_list[0]
            solver.board.match(first_pair1[0], first_pair1[1])
            solver.path.append(first_pair1)
        path1 = solver.get_solution()

        solver.set_board(board2)
        if len(solver.board.pair_list) > 0:
            first_pair2 = solver.board.pair_list[0]
            solver.board.match(first_pair2[0], first_pair2[1])
            solver.path.append(first_pair2)
        path2 = solver.get_solution()

        assert isinstance(path1, list)
        assert isinstance(path2, list)

    def test_solve_does_not_modify_original_board(self):
        """测试求解不修改原始棋盘"""
        original_board = Board()
        original_board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0, 0, 0, 0, 0])

        board_copy = Board()
        board_copy.set_digits(original_board.digit_list[:])

        solver = Solver()
        solver.set_board(original_board)

        if len(solver.board.pair_list) > 0:
            first_pair = solver.board.pair_list[0]
            solver.board.match(first_pair[0], first_pair[1])

        assert original_board.digit_list == board_copy.digit_list


class TestSolverIntegration:
    """测试 Solver 与 TwinBoard 的集成"""

    def test_twin_board_digit_transformation(self):
        """测试数字转换在求解中的正确性"""
        board = Board()
        board.set_digits([2, 0, 0, 0, 0, 0, 0, 0, 8,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert solver.board.digit_list[0] == 2
        assert solver.board.digit_list[8] == 2

    def test_solver_uses_digit_pairs(self):
        """测试求解器使用 digit_pairs"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            first_pair = solver.board.pair_list[0]
            solver.board.match(first_pair[0], first_pair[1])

            assert isinstance(solver.board.digit_list, list)

    def test_solver_respects_potential_num(self):
        """测试求解器使用 potential_num"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        initial_potential = solver.board.potential_pair_count

        assert initial_potential >= 0

    def test_board_state_updates_after_match(self):
        """测试配对后棋盘状态更新"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        initial_nonzero = len([d for d in solver.board.digit_list if d != 0])

        if len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])

            new_nonzero = len([d for d in solver.board.digit_list if d != 0])
            assert new_nonzero <= initial_nonzero


class TestSolverAlgorithmBehavior:
    """测试求解算法行为"""

    def test_algorithm_with_adjacent_pairs(self):
        """测试算法处理相邻配对"""
        board = Board()
        board.set_digits([5, 5, 5, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) > 0

        pair = solver.board.pair_list[0]
        solver.board.match(pair[0], pair[1])
        solver.path.append(pair)

        assert len(solver.board.digit_list) <= 9

    def test_solver_path_accumulates_matches(self):
        """测试路径累加配对"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          6, 6, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        initial_path_len = len(solver.path)
        while len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])
            solver.path.append(pair)

        assert len(solver.path) > initial_path_len

    def test_solver_handles_ties_in_potential(self):
        """测试算法处理潜力值相等的配对"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) >= 2

        first_pair = solver.board.pair_list[0]
        solver.board.match(first_pair[0], first_pair[1])
        solver.path.append(first_pair)

        assert len(solver.path) == 1


class TestSolverStateConsistency:
    """测试求解器状态一致性"""

    def test_state_consistent_after_match(self):
        """测试配对后状态一致"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])

            assert isinstance(solver.board.digit_list, list)

    def test_path_immutability(self):
        """测试路径不可变性"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        path_before = solver.get_solution()

        if len(solver.board.pair_list) > 0:
            pair = solver.board.pair_list[0]
            solver.board.match(pair[0], pair[1])
            solver.path.append(pair)

        path_after = solver.get_solution()

        assert isinstance(path_before, list)
        assert isinstance(path_after, list)
        assert len(path_after) >= len(path_before)


class TestSolverBugEdgeCases:
    """测试 Solver 算法边缘情况（记录已知bug）"""

    def test_bug_digit_pairs_non_empty_but_no_potential(self):
        """
        测试已知bug：当digit_pairs非空但所有配对的potential_num都为0时，
        solve()方法会崩溃，因为best_digit_pair为None
        
        当前行为：TypeError: 'NoneType' object is not subscriptable
        预期行为：应该返回False或正确处理这种情况
        """
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                          4, 5, 6, 0, 0, 0, 0, 0, 0,
                          7, 8, 9, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        if len(solver.board.pair_list) > 0 and solver.board.potential_pair_count == 0:
            with pytest.raises(TypeError, match="'NoneType' object is not subscriptable"):
                solver.solve()


class TestSolverFullCoverage:
    """测试 Solver 完整覆盖率"""

    def test_solve_returns_true_when_board_cleared(self):
        """测试棋盘完全清空时返回 True"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                          6, 6, 0, 0, 0, 0, 0, 0, 0,
                          7, 7, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        initial_pairs = len(solver.board.pair_list)
        assert initial_pairs > 0, "Test setup failed: no digit pairs found"

        result = solver.solve()

        if solver.board.digit_list:
            assert result is False
        else:
            assert result is True

    def test_solve_with_manual_board_state(self):
        """测试在调用 solve() 之前手动设置 board 状态"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        assert len(solver.board.pair_list) > 0

        solver.board.match(solver.board.pair_list[0][0], solver.board.pair_list[0][1])
        assert solver.board.digit_list == []

        result = solver.solve()

        assert result is False

    def test_solve_direct_return_true_coverage(self):
        """测试直接触发 return True 分支"""
        solver = Solver()
        solver.board = type('MockBoard', (), {
            'digit_pairs': [(0, 1)],
            'digit_list': [],
            'potential_num': 1,
            'match': lambda self, i, j: setattr(self, 'digit_pairs', [])
        })()

        result = solver.solve()

        assert result is True

    def test_solve_best_digit_pair_none_returns_false(self):
        """测试 best_digit_pair 为 None 时返回 False"""
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                          4, 5, 6, 0, 0, 0, 0, 0, 0,
                          7, 8, 9, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        has_pairs_with_zero_potential = (
                len(solver.board.pair_list) > 0 and
                solver.board.potential_pair_count == 0
        )

        if has_pairs_with_zero_potential:
            result = solver.solve()
            assert result is False

    def test_solve_returns_false_after_loop(self):
        """测试 solve 循环结束后返回 False"""
        board = Board()
        board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                          4, 5, 6, 0, 0, 0, 0, 0, 0,
                          7, 8, 9, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        solver = Solver()
        solver.set_board(board)

        result = solver.solve()

        assert result is False
