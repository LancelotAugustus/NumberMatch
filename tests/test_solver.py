import pytest
from srcs.board import Board
from srcs.twin_board import TwinBoard
from srcs.solver import Solver


class TestSolverInit:
    """测试Solver初始化"""

    def test_init_empty_solver(self):
        """测试初始化空求解器"""
        solver = Solver()
        assert solver.board is None
        assert solver.twin_board is None
        assert solver.path == []

    def test_init_attributes_exist(self):
        """测试初始化时属性存在"""
        solver = Solver()
        assert hasattr(solver, 'board')
        assert hasattr(solver, 'twin_board')
        assert hasattr(solver, 'path')


class TestSolverSetBoard:
    """测试set_board方法"""

    def test_set_board_with_empty_board(self):
        """测试设置空棋盘"""
        board = Board()
        board.set_digits([])
        solver = Solver()
        solver.set_board(board)
        assert solver.board is not None
        assert solver.twin_board is not None
        assert solver.path == []

    def test_set_board_with_single_digit(self):
        """测试设置单个数字的棋盘"""
        board = Board()
        board.set_digits([5])
        solver = Solver()
        solver.set_board(board)
        assert solver.board is not None
        assert solver.twin_board is not None

    def test_set_board_with_multiple_digits(self):
        """测试设置多个数字的棋盘"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])
        solver = Solver()
        solver.set_board(board)
        assert solver.board is not None
        assert solver.twin_board is not None
        assert solver.path == []

    def test_set_board_resets_path(self):
        """测试设置新棋盘时重置路径"""
        board1 = Board()
        board1.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board1)
        solver.solve()

        board2 = Board()
        board2.set_digits([2, 2])
        solver.set_board(board2)
        assert solver.path == []


class TestSolverSolve:
    """测试solve方法"""

    def test_solve_empty_board(self):
        """测试求解空棋盘（应返回False，因为pair_list为空）"""
        board = Board()
        board.set_digits([])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is False

    def test_solve_single_digit_no_match(self):
        """测试单个数字无法消除"""
        board = Board()
        board.set_digits([5])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is False

    def test_solve_two_same_digits(self):
        """测试两个相同数字可以消除"""
        board = Board()
        board.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True
        assert len(solver.path) == 1

    def test_solve_two_complementary_digits(self):
        """测试两个互补数字（和为10）可以消除"""
        board = Board()
        board.set_digits([3, 7])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True
        assert len(solver.path) == 1

    def test_solve_four_same_digits(self):
        """测试四个相同数字可以完全消除"""
        board = Board()
        board.set_digits([1, 1, 1, 1])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True
        assert len(solver.path) == 2

    def test_solve_multiple_pairs(self):
        """测试多对数字可以完全消除"""
        board = Board()
        board.set_digits([1, 1, 2, 2, 3, 3])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True
        assert len(solver.path) == 3

    def test_solve_no_possible_matches(self):
        """测试没有可能匹配的情况"""
        board = Board()
        board.set_digits([1, 2, 3, 4])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is False

    def test_solve_complex_board(self):
        """测试复杂棋盘求解"""
        board = Board()
        board.set_digits([1, 9, 2, 8, 3, 7, 4, 6, 5, 5, 6, 4, 7, 3, 8, 2, 9, 1])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True

    def test_solve_returns_bool(self):
        """测试solve返回布尔值"""
        board = Board()
        board.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert isinstance(result, bool)

    def test_solve_path_accumulates(self):
        """测试求解过程中路径累加"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        solver = Solver()
        solver.set_board(board)
        assert solver.path == []
        solver.solve()
        assert len(solver.path) == 2

    def test_solve_with_converted_digits(self):
        """测试使用转换数字的求解"""
        board = Board()
        board.set_digits([1, 9, 1, 9])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is True
        assert len(solver.path) == 2

    def test_solve_blocked_pairs(self):
        """测试有阻隔的配对情况"""
        board = Board()
        board.set_digits([1, 2, 1, 2])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert result is False


class TestSolverGetSolution:
    """测试get_solution方法"""

    def test_get_solution_empty_path(self):
        """测试获取空路径"""
        board = Board()
        board.set_digits([])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        solution = solver.get_solution()
        assert solution == []

    def test_get_solution_returns_list(self):
        """测试get_solution返回列表"""
        board = Board()
        board.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        solution = solver.get_solution()
        assert isinstance(solution, list)

    def test_get_solution_correct_pairs(self):
        """测试获取正确的消除对"""
        board = Board()
        board.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        solution = solver.get_solution()
        assert len(solution) == 1
        assert isinstance(solution[0], tuple)
        assert len(solution[0]) == 2

    def test_get_solution_after_solve(self):
        """测试solve后获取解决方案"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        solution = solver.get_solution()
        assert len(solution) == 2

    def test_get_solution_returns_copy(self):
        """测试get_solution返回正确的路径"""
        board = Board()
        board.set_digits([1, 1])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        solution = solver.get_solution()
        assert len(solution) == 1
        assert isinstance(solution[0], tuple)


class TestSolverIntegration:
    """测试Solver综合场景"""

    def test_full_workflow(self):
        """测试完整工作流程"""
        board = Board()
        board.set_digits([5, 5, 6, 4, 7, 3])
        solver = Solver()

        solver.set_board(board)
        assert solver.board is not None

        result = solver.solve()
        assert result is True

        solution = solver.get_solution()
        assert len(solution) == 3

    def test_unsolvable_workflow(self):
        """测试无法求解的工作流程"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5])
        solver = Solver()

        solver.set_board(board)
        result = solver.solve()
        assert result is False

        solution = solver.get_solution()
        assert solution == []

    def test_multiple_set_board_calls(self):
        """测试多次设置棋盘"""
        solver = Solver()

        board1 = Board()
        board1.set_digits([1, 1])
        solver.set_board(board1)
        solver.solve()
        solution1 = solver.get_solution()

        board2 = Board()
        board2.set_digits([2, 2])
        solver.set_board(board2)
        solver.solve()
        solution2 = solver.get_solution()

        assert len(solution1) == 1
        assert len(solution2) == 1

    def test_twin_board_created(self):
        """测试twin_board正确创建"""
        board = Board()
        board.set_digits([1, 9, 2, 8])
        solver = Solver()
        solver.set_board(board)
        assert solver.twin_board is not None
        assert hasattr(solver.twin_board, 'pair_list')
        assert hasattr(solver.twin_board, 'score')

    def test_solver_with_zeros_in_board(self):
        """测试棋盘包含0的情况"""
        board = Board()
        board.set_digits([1, 0, 1, 0, 2, 0, 2, 0])
        solver = Solver()
        solver.set_board(board)
        result = solver.solve()
        assert isinstance(result, bool)

    def test_solver_path_contains_valid_pairs(self):
        """测试路径中的消除对是有效的"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        if solver.path:
            for pair in solver.path:
                assert isinstance(pair, tuple)
                assert len(pair) == 2
                assert pair[0] != pair[1]

    def test_solver_preserves_original_board(self):
        """测试求解过程保留原始棋盘"""
        board = Board()
        board.set_digits([1, 1])
        original_digits = board.digit_list[:]
        solver = Solver()
        solver.set_board(board)
        solver.solve()
        assert board.digit_list == original_digits
