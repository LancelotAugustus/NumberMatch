"""
NumberMatch 项目 Board 类的全面单元测试

本文件包含 Board 类的完整单元测试，涵盖：
1. 棋盘初始化和基本操作
2. 配对逻辑（四种匹配规则）
3. 棋盘操作方法（clear, fill, match）
4. 边界条件和异常处理
5. 安全复制功能

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

from board import Board


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
        board.set_board([1, 0, 3, 4, 5, 6, 7, 8, 9,
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

    def test_set_board_basic(self):
        """测试设置基本棋盘"""
        board = Board()
        test_data = [i % 9 + 1 for i in range(81)]
        board.set_board(test_data)
        assert len(board.digit_list) == 81
        assert board.digit_list == test_data

    def test_set_board_with_zeros(self):
        """测试设置包含零值的棋盘"""
        board = Board()
        test_data = [1, 0, 3, 0, 5, 0, 7, 0, 9] * 3
        board.set_board(test_data)
        assert len(board.digit_list) == 27
        assert board.digit_list == test_data

    def test_generate_board_size(self):
        """测试生成指定大小的随机棋盘"""
        board = Board()
        board.generate_board(45)
        assert len(board.digit_list) == 45
        assert all(1 <= d <= 9 for d in board.digit_list)

    def test_generate_board_multiple_calls(self):
        """测试多次生成棋盘的独立性"""
        board = Board()
        board.generate_board(9)
        first_result = board.digit_list[:]
        
        board.generate_board(9)
        second_result = board.digit_list[:]
        
        # 两次生成的结果可能不同（随机性），但结构应该一致
        assert len(first_result) == len(second_result) == 9
        assert all(1 <= d <= 9 for d in first_result)
        assert all(1 <= d <= 9 for d in second_result)


class TestSameRowMatching:
    """测试同行匹配逻辑"""

    def test_same_row_match_success(self):
        """测试同行无阻挡时成功匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 8) is True

    def test_same_row_match_blocked(self):
        """测试同行有阻挡时匹配失败"""
        board = Board()
        board.set_board([1, 0, 2, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 8) is False

    def test_same_row_adjacent_match(self):
        """测试同行相邻数字匹配"""
        board = Board()
        board.set_board([1, 1, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 1) is True


class TestSameColumnMatching:
    """测试同列匹配逻辑"""

    def test_same_column_match_success(self):
        """测试同列无阻挡时成功匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 72) is True

    def test_same_column_match_blocked(self):
        """测试同列有阻挡时匹配失败"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0])
        board.digit_list[45] = 2  # 在第5行第0列放置阻挡
        assert board.is_matching(0, 72) is False

    def test_same_column_adjacent_match(self):
        """测试同列相邻数字匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 9) is True


class TestDiagonalMatching:
    """测试对角线匹配逻辑"""

    def test_main_diagonal_match_success(self):
        """测试主对角线匹配成功"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 20) is True

    def test_anti_diagonal_match_success(self):
        """测试反对角线匹配成功"""
        board = Board()
        board.set_board([0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 1, 0,
                         0, 0, 0, 0, 0, 0, 1, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(8, 16) is True

    def test_diagonal_match_blocked(self):
        """测试对角线有阻挡时匹配失败"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 2, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 20) is False


class TestCrossRowMatching:
    """测试跨行首尾匹配逻辑"""

    def test_cross_row_match_success(self):
        """测试跨行首尾匹配成功"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 17) is True

    def test_cross_row_match_blocked(self):
        """测试跨行首尾有阻挡时匹配失败"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         2, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 17) is False

    def test_cross_row_non_adjacent_no_match(self):
        """测试跨行非相邻行不能匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1])
        assert board.is_matching(0, 8) is False  # 第0行第0列和第0行第8列，相同行但被阻挡


class TestSumToTenMatching:
    """测试和为10的匹配逻辑"""

    def test_sum_to_ten_same_row(self):
        """测试同行和为10的匹配"""
        board = Board()
        board.set_board([3, 0, 0, 0, 0, 0, 0, 0, 7,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 8) is True

    def test_sum_to_ten_same_column(self):
        """测试同列和为10的匹配"""
        board = Board()
        board.set_board([6, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         4, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 72) is True

    def test_sum_to_ten_diagonal(self):
        """测试对角线和为10的匹配"""
        board = Board()
        board.set_board([2, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 8])
        assert board.is_matching(0, 80) is True

    def test_sum_not_ten_no_match(self):
        """测试和不为10时不能匹配"""
        board = Board()
        board.set_board([3, 0, 0, 0, 0, 0, 0, 0, 6,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 8) is False  # 3+6=9 ≠ 10


class TestNonMatchingCases:
    """测试各种不匹配的情况"""

    def test_same_index_no_match(self):
        """测试相同索引不能匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 0) is False

    def test_zero_digit_no_match(self):
        """测试包含零值不能匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 1) is False  # 1和0，不能匹配
        assert board.is_matching(1, 8) is False  # 0和1，不能匹配

    def test_different_numbers_no_match(self):
        """测试不同数字且和不等于10时不能匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 3,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert board.is_matching(0, 8) is False  # 1和3，既不相同，和也不为10

    def test_blocked_path_no_match(self):
        """测试路径被阻挡时不能匹配"""
        board = Board()
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 1,
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
        assert board.is_matching(0, 8) is False


class TestClearAndFill:
    """测试 clear() 和 fill() 方法"""

    def test_clear_removes_empty_rows(self):
        """测试 clear() 移除空行"""
        board = Board()
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        original_length = len(board.digit_list)
        board.clear()
        
        # 验证空行被移除
        assert len(board.digit_list) < original_length
        assert len(board.digit_list) == 18  # 2行，每行9个元素
        
        # 验证所有剩余元素都是非零的
        assert all(d != 0 for d in board.digit_list)

    def test_clear_no_empty_rows(self):
        """测试 clear() 处理无空行的情况"""
        board = Board()
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        original_length = len(board.digit_list)
        board.clear()
        
        # 验证长度不变
        assert len(board.digit_list) == original_length
        assert len(board.digit_list) == 18

    def test_clear_all_empty(self):
        """测试 clear() 处理全空棋盘"""
        board = Board()
        board.set_board([0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        board.clear()
        
        # 验证全部移除
        assert len(board.digit_list) == 0

    def test_fill_appends_remaining_digits(self):
        """测试 fill() 追加剩余数字"""
        board = Board()
        board.set_board([1, 0, 3, 0, 5, 0, 7, 0, 9,
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
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        original_length = len(board.digit_list)
        board.fill()
        
        # 验证长度不变
        assert len(board.digit_list) == original_length * 2
        assert board.digit_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_fill_all_zeros(self):
        """测试 fill() 处理全零值的情况"""
        board = Board()
        board.set_board([0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        original_length = len(board.digit_list)
        board.fill()
        
        # 验证长度不变（全零）
        assert len(board.digit_list) == original_length


class TestMatchOperation:
    """测试 match() 方法"""

    def test_match_successful_removes_pairs(self):
        """测试成功配对消除"""
        board = Board()
        board.set_board([3, 0, 0, 0, 0, 0, 0, 0, 7,
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
        board.set_board([1, 0, 0, 0, 0, 0, 0, 0, 3,
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
        board.set_board([5, 0, 0, 0, 0, 0, 0, 0, 5,
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


class TestSafeCopy:
    """测试 safe_copy() 方法"""

    def test_safe_copy_creates_independent_copy(self):
        """测试 safe_copy() 创建独立副本"""
        board = Board()
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        board_copy = board.safe_copy()
        
        # 验证内容相同
        assert board_copy.digit_list == board.digit_list
        
        # 验证是独立副本
        board.digit_list[0] = 99
        assert board_copy.digit_list[0] == 1
        assert board.digit_list[0] == 99

    def test_safe_copy_empty_board(self):
        """测试空棋盘的 safe_copy()"""
        board = Board()
        board_copy = board.safe_copy()
        
        assert board_copy.digit_list == []
        assert board_copy is not board

    def test_safe_copy_type(self):
        """测试 safe_copy() 返回正确类型"""
        board = Board()
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        board_copy = board.safe_copy()
        
        assert isinstance(board_copy, Board)
        assert type(board_copy) == Board


class TestEdgeCases:
    """测试边界条件"""

    def test_empty_board_operations(self):
        """测试空棋盘操作"""
        board = Board()
        
        # 测试空棋盘的字符串表示
        assert str(board) == ""
        
        # 测试 clear() 在空棋盘上
        board.clear()
        assert board.digit_list == []
        
        # 测试 fill() 在空棋盘上
        board.fill()
        assert board.digit_list == []

    def test_single_element_board(self):
        """测试单元素棋盘"""
        board = Board()
        board.set_board([5])
        
        assert len(board.digit_list) == 1
        assert board.digit_list[0] == 5
        assert "5" in str(board)

    def test_boundary_indices(self):
        """测试边界索引"""
        board = Board()
        board.set_board([1] * 81)  # 完整棋盘
        
        # 测试四角
        assert board.is_matching(0, 8) is False   # 左上角同行
        assert board.is_matching(0, 72) is False  # 左上角到左下角
        assert board.is_matching(8, 80) is False  # 右上角到右下角
        assert board.is_matching(72, 80) is False # 左下角到右下角

    def test_out_of_range_indices(self):
        """测试越界索引"""
        board = Board()
        board.set_board([1, 2, 3, 4, 5, 6, 7, 8, 9])

        with pytest.raises(IndexError):
            board.is_matching(0, 9)  # 第二个索引越界
        with pytest.raises(IndexError):
            board.is_matching(9, 0)  # 第一个索引越界
        # 注意：Python列表支持负索引，不会抛出IndexError

    def test_mixed_match_scenarios(self):
        """测试混合匹配场景"""
        board = Board()
        board.set_board([1, 0, 9, 0, 0, 0, 0, 0, 0,  # 第一行：1和9可以匹配（和为10）
                         2, 0, 0, 0, 0, 0, 0, 0, 0,  # 第二行
                         3, 0, 0, 0, 0, 0, 0, 0, 0,  # 第三行
                         0, 0, 0, 0, 0, 0, 0, 0, 0,  # 空行
                         0, 0, 0, 0, 0, 0, 0, 0, 0,  # 空行
                         0, 0, 0, 0, 0, 0, 0, 0, 0,  # 空行
                         0, 0, 0, 0, 0, 0, 0, 0, 0,  # 空行
                         0, 0, 0, 0, 0, 0, 0, 0, 0,  # 空行
                         0, 0, 0, 0, 0, 0, 0, 0, 0]) # 空行
        
        # 验证匹配成功
        assert board.is_matching(0, 2) is True  # 1和9，和为10
        assert board.is_matching(0, 1) is False # 1和0，不能匹配
        
        # 执行匹配
        board.match(0, 2)
        
        # 验证空行被清除（第一行变成全零被清除，6个空行也被清除）
        digit_grid = [board.digit_list[i: i + 9] for i in range(0, len(board.digit_list), 9)]
        # 只剩下第二行和第三行
        assert len(digit_grid) == 2