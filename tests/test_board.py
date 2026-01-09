"""
NumberMatch 项目 Board 类的全面单元测试

本文件包含 Board 类的完整单元测试，涵盖：
1. 棋盘初始化和基本操作
2. 配对逻辑（四种匹配规则）
3. 棋盘操作方法（clear, fill, match）
4. 边界条件和异常处理

使用方法：
    pytest tests/test_board.py -v          # 详细输出
    pytest tests/test_board.py --cov       # 查看覆盖率
    pytest tests/test_board.py -k "match"  # 运行特定测试
"""

import pytest
import sys
from pathlib import Path

# 将 srcs 目录添加到 Python 路径，确保能够导入 Board 类
SRCS_PATH = Path(__file__).parent.parent / "srcs"
if str(SRCS_PATH) not in sys.path:
    sys.path.insert(0, str(SRCS_PATH))

from srcs.board import Board


class TestBoardInitialization:
    """测试 Board 类的初始化功能"""

    def test_init_empty_board(self):
        """测试初始化空棋盘"""
        board = Board()
        assert board.digit_list == []
        assert len(board.digit_list) == 0

    def test_str_representation_empty(self):
        """测试空棋盘的字符串表示"""
        board = Board()
        board_str = str(board)
        assert board_str == ""

    def test_str_representation_with_numbers(self):
        """测试有数字的棋盘字符串表示"""
        board = Board()
        board.set_digits([1, 0, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 2, 3, 4, 5, 6, 7, 8, 9])
        board_str = str(board)
        lines = board_str.split('\n')
        assert len(lines) == 3
        assert "1 . 3 4 5 6 7 8 9" in board_str
        assert "1 2 3 4 5 6 7 8 9" in board_str
        assert "." in board_str  # 验证零值被替换为.


class TestBoardSetup:
    """测试棋盘设置功能"""

    def test_set_digits_basic(self):
        """测试设置基本棋盘"""
        board = Board()
        test_data = [i % 9 + 1 for i in range(81)]
        board.set_digits(test_data)
        assert len(board.digit_list) == 81
        assert board.digit_list == test_data

    def test_set_digits_with_zeros(self):
        """测试设置包含零值的棋盘"""
        board = Board()
        test_data = [1, 0, 3, 0, 5, 0, 7, 0, 9] * 3
        board.set_digits(test_data)
        assert len(board.digit_list) == 27
        assert board.digit_list == test_data


class TestSameRowMatching:
    """测试同行匹配逻辑"""

    def test_same_row_match_success(self):
        """测试同行无阻挡时成功匹配"""
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
        assert board._is_matching(0, 8) is True

    def test_same_row_match_blocked(self):
        """测试同行有阻挡时匹配失败"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 8) is False

    def test_same_row_adjacent_match(self):
        """测试同行相邻数字匹配"""
        board = Board()
        board.set_digits([1, 1, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 1) is True


class TestSameColumnMatching:
    """测试同列匹配逻辑"""

    def test_same_column_match_success(self):
        """测试同列无阻挡时成功匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 72) is True

    def test_same_column_match_blocked(self):
        """测试同列有阻挡时匹配失败"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0])
        board.digit_list[45] = 2  # 在第5行第0列放置阻挡
        assert board._is_matching(0, 72) is False

    def test_same_column_adjacent_match(self):
        """测试同列相邻数字匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 9) is True


class TestDiagonalMatching:
    """测试对角线匹配逻辑"""

    def test_main_diagonal_match_success(self):
        """测试主对角线匹配成功"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 20) is True

    def test_anti_diagonal_match_success(self):
        """测试反对角线匹配成功"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 1, 0,
                         0, 0, 0, 0, 0, 0, 1, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(8, 16) is True

    def test_diagonal_match_blocked(self):
        """测试对角线有阻挡时匹配失败"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 2, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 20) is False


class TestCrossRowMatching:
    """测试跨行首尾匹配逻辑"""

    def test_cross_row_match_success(self):
        """测试跨行首尾匹配成功"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 17) is True

    def test_cross_row_match_blocked(self):
        """测试跨行首尾有阻挡时匹配失败"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         2, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 17) is False

    def test_cross_row_non_adjacent_no_match(self):
        """测试跨行非相邻行不能匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1])
        assert board._is_matching(0, 8) is False  # 第0行第0列和第0行第8列，相同行但被阻挡


class TestSumToTenMatching:
    """测试和为10的匹配逻辑"""

    def test_sum_to_ten_same_row(self):
        """测试同行和为10的匹配"""
        board = Board()
        board.set_digits([3, 0, 0, 0, 0, 0, 0, 0, 7,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 8) is True

    def test_sum_to_ten_same_column(self):
        """测试同列和为10的匹配"""
        board = Board()
        board.set_digits([6, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         4, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 72) is True

    def test_sum_to_ten_diagonal(self):
        """测试对角线和为10的匹配"""
        board = Board()
        board.set_digits([2, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 8])
        assert board._is_matching(0, 80) is True

    def test_sum_not_ten_no_match(self):
        """测试和不为10时不能匹配"""
        board = Board()
        board.set_digits([3, 0, 0, 0, 0, 0, 0, 0, 6,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 8) is False  # 3+6=9 ≠ 10


class TestNonMatchingCases:
    """测试各种不匹配的情况"""

    def test_same_index_no_match(self):
        """测试相同索引不能匹配"""
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
        assert board._is_matching(0, 0) is False

    def test_zero_digit_no_match(self):
        """测试包含零值不能匹配"""
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
        assert board._is_matching(0, 1) is False  # 1和0，不能匹配
        assert board._is_matching(1, 8) is False  # 0和1，不能匹配

    def test_different_numbers_no_match(self):
        """测试不同数字且和不等于10时不能匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 3,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 8) is False  # 1和3，既不相同，和也不为10

    def test_blocked_path_no_match(self):
        """测试路径被阻挡时不能匹配"""
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
        # 虽然1和1相同，但路径被阻挡（在索引1,2,3,4,5,6,7处有阻挡）
        board.digit_list[3] = 2  # 在中间添加阻挡
        assert board._is_matching(0, 8) is False


class TestClearAndFill:
    """测试 clear() 和 fill() 方法"""

    def test_clear_removes_empty_rows(self):
        """测试 clear() 移除空行"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        original_length = len(board.digit_list)
        board._clear()

        # 验证空行被移除
        assert len(board.digit_list) < original_length
        assert len(board.digit_list) == 18  # 2行，每行9个元素

        # 验证所有剩余元素都是非零的
        assert all(d != 0 for d in board.digit_list)

    def test_clear_no_empty_rows(self):
        """测试 clear() 处理无空行的情况"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         1, 2, 3, 4, 5, 6, 7, 8, 9])

        original_length = len(board.digit_list)
        board._clear()

        # 验证长度不变
        assert len(board.digit_list) == original_length
        assert len(board.digit_list) == 18

    def test_clear_all_empty(self):
        """测试 clear() 处理全空棋盘"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        board._clear()

        # 验证全部移除
        assert len(board.digit_list) == 0

    def test_fill_appends_remaining_digits(self):
        """测试 fill() 追加剩余数字"""
        board = Board()
        board.set_digits([1, 0, 3, 0, 5, 0, 7, 0, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 2, 3, 4, 5, 6, 7, 8, 9])

        original_length = len(board.digit_list)
        original_nonzero = [d for d in board.digit_list if d != 0]

        board.fill()

        # 验证长度增加
        assert len(board.digit_list) == original_length + len(original_nonzero)

        # 验证末尾包含所有原始非零数字
        assert board.digit_list[-len(original_nonzero):] == original_nonzero

    def test_fill_no_zeros(self):
        """测试 fill() 处理无零值的情况"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])

        original_length = len(board.digit_list)
        board.fill()

        # 验证长度不变
        assert len(board.digit_list) == original_length * 2
        assert board.digit_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_fill_all_zeros(self):
        """测试 fill() 处理全零值的情况"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 0])

        original_length = len(board.digit_list)
        board.fill()

        # 验证长度不变（全零）
        assert len(board.digit_list) == original_length


class TestMatchOperation:
    """测试 match() 方法"""

    def test_match_successful_removes_pairs(self):
        """测试成功配对消除"""
        board = Board()
        board.set_digits([3, 0, 0, 0, 0, 0, 0, 0, 7,
                         1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        board.match(0, 8)  # 3+7=10，匹配

        # 验证空行被清除，只保留第二行
        digit_grid = [board.digit_list[i: i + 9] for i in range(0, len(board.digit_list), 9)]
        assert len(digit_grid) == 1
        assert digit_grid[0] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # 验证配对后第一行已被完全清除（因为全部为0）
        assert len(board.digit_list) == 9

    def test_match_unsuccessful_no_removal(self):
        """测试不成功配对时不消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 3,
                         1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        original_digit_list = board.digit_list[:]
        board.match(0, 8)  # 1+3=4，不能匹配

        # 验证数据未改变
        assert board.digit_list == original_digit_list

    def test_match_with_different_match_types(self):
        """测试不同类型的匹配都能正确消除"""
        board = Board()
        board.set_digits([5, 0, 0, 0, 0, 0, 0, 0, 5,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        board.match(0, 8)  # 5和5相同，匹配

        # 验证空行被清除（第一行被移除）
        digit_grid = [board.digit_list[i: i + 9] for i in range(0, len(board.digit_list), 9)]
        assert len(digit_grid) == 0  # 第一行被完全移除


class TestEdgeCases:
    """测试边界条件"""

    def test_empty_board_operations(self):
        """测试空棋盘操作"""
        board = Board()

        assert str(board) == ""

        board._clear()
        assert board.digit_list == []

        board.fill()
        assert board.digit_list == []

    def test_single_element_board(self):
        """测试单元素棋盘"""
        board = Board()
        board.set_digits([5])

        assert len(board.digit_list) == 1
        assert board.digit_list[0] == 5
        assert "5" in str(board)

    def test_boundary_indices(self):
        """测试边界索引"""
        board = Board()
        board.set_digits([1] * 81)

        assert board._is_matching(0, 8) is False
        assert board._is_matching(0, 72) is False
        assert board._is_matching(8, 80) is False
        assert board._is_matching(72, 80) is False

    def test_out_of_range_indices(self):
        """测试越界索引"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])

        with pytest.raises(IndexError):
            board._is_matching(0, 9)
        with pytest.raises(IndexError):
            board._is_matching(9, 0)

    def test_mixed_match_scenarios(self):
        """测试混合匹配场景"""
        board = Board()
        board.set_digits([1, 0, 9, 0, 0, 0, 0, 0, 0,
                         2, 0, 0, 0, 0, 0, 0, 0, 0,
                         3, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        assert board._is_matching(0, 2) is True
        assert board._is_matching(0, 1) is False

        board.match(0, 2)

        digit_grid = [board.digit_list[i: i + 9] for i in range(0, len(board.digit_list), 9)]
        assert len(digit_grid) == 2


class TestCanMatchMethod:
    """测试 _can_match 方法"""

    def test_can_match_same_digits(self):
        """测试相同数字可以匹配"""
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
        assert board._can_match(0, 8) is True

    def test_can_match_sum_to_ten(self):
        """测试和为10的数字可以匹配"""
        board = Board()
        board.set_digits([3, 0, 0, 0, 0, 0, 0, 0, 7,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._can_match(0, 8) is True

    def test_can_match_cannot_match(self):
        """测试不同数字且和不等于10时不能匹配"""
        board = Board()
        board.set_digits([2, 0, 0, 0, 0, 0, 0, 0, 5,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._can_match(0, 8) is False

    def test_can_match_with_zeros(self):
        """测试包含0时不能匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._can_match(0, 1) is False
        assert board._can_match(1, 8) is False


class TestDiagonalDirections:
    """测试对角线方向"""

    def test_main_diagonal_adjacent(self):
        """测试相邻主对角线匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 1, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 10) is True
        assert board._is_matching(10, 11) is False

    def test_main_diagonal_blocked(self):
        """测试主对角线被阻挡"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 2, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 20) is False

    def test_anti_diagonal_adjacent(self):
        """测试相邻反对角线匹配"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 1, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(8, 16) is True
        assert board._is_matching(16, 17) is False

    def test_anti_diagonal_blocked(self):
        """测试反对角线被阻挡"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 2, 0, 0,
                         0, 0, 0, 0, 0, 1, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(8, 24) is False


class TestClearAndFillCombinations:
    """测试 clear() 和 fill() 的组合操作"""

    def test_clear_with_partial_rows(self):
        """测试 clear() 保留部分非空行"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3, 0, 4, 0, 5,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         6, 7, 8, 9, 1, 2, 3, 4, 5])

        board._clear()

        assert len(board.digit_list) == 18

    def test_fill_then_clear(self):
        """测试 fill() 追加非零数字"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3, 0, 4, 0, 5])

        board.fill()

        assert len(board.digit_list) == 14

    def test_single_match_then_clear(self):
        """测试单次配对后清理"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         2, 0, 0, 0, 0, 0, 0, 0, 2,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         3, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        board.match(0, 8)
        board._clear()

        nonzero_count = len([d for d in board.digit_list if d != 0])
        assert nonzero_count >= 2


class TestCrossRowExtended:
    """测试跨行首尾匹配的扩展场景"""

    def test_cross_row_adjacent_only(self):
        """测试跨行仅相邻行可以匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board._is_matching(0, 17) is True

    def test_cross_row_non_adjacent_no_match(self):
        """测试跨行非相邻行不能匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 2])

        assert board._is_matching(0, 80) is False
        assert board._is_matching(0, 17) is False
        assert board._is_matching(8, 72) is False


class TestMatchDataStructure:
    """测试配对后的数据结构验证"""

    def test_match_removes_correct_elements(self):
        """测试配对后正确移除元素"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         1, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        original_count_nonzero = len([d for d in board.digit_list if d != 0])

        board.match(9, 17)

        new_count_nonzero = len([d for d in board.digit_list if d != 0])
        assert new_count_nonzero == original_count_nonzero - 2

    def test_consecutive_matches_reduce_size(self):
        """测试连续配对减少棋盘大小"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 9,
                         2, 0, 0, 0, 0, 0, 0, 0, 8,
                         3, 0, 0, 0, 0, 0, 0, 0, 7,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        initial_len = len(board.digit_list)

        board.match(0, 8)
        assert len(board.digit_list) < initial_len

    def test_partial_row_match_preserves_row(self):
        """测试部分行配对保留行"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                         2, 3, 4, 5, 6, 7, 8, 9, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        board.match(0, 8)

        assert len(board.digit_list) >= 9


class TestAllMatchTypesCombined:
    """测试所有匹配类型的组合场景"""

    def test_complex_board_individual_matches(self):
        """测试复杂棋盘各类型匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 9,
                         0, 5, 0, 0, 0, 0, 0, 5, 0,
                         0, 0, 3, 0, 0, 0, 3, 0, 0,
                         0, 0, 0, 7, 0, 7, 0, 0, 0,
                         0, 0, 0, 0, 4, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])

        assert board._is_matching(0, 8) is True
        assert board._is_matching(10, 16) is True

    def test_same_digit_adjacent_matches(self):
        """测试相同数字的相邻匹配"""
        board = Board()
        board.set_digits([5, 5, 0, 0, 0, 0, 0, 0, 0,
                         5, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 5, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 5, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 5, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 5, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 5, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 5, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 5])

        assert board._is_matching(0, 1) is True
        assert board._is_matching(0, 9) is True
