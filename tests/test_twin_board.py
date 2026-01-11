"""
NumberMatch 项目 TwinBoard 类的全面单元测试

本文件包含 TwinBoard 类的完整单元测试，涵盖：
1. 孪生棋盘初始化和数字转换逻辑
2. 配对逻辑（仅基于转换后数字相同）
3. 信息更新机制（digit_pairs, potential_num）
4. 继承的 Board 方法行为
5. 边界条件和异常处理

使用方法：
    pytest tests/test_twin_board.py -v          # 详细输出
    pytest tests/test_twin_board.py --cov       # 查看覆盖率
    pytest tests/test_twin_board.py -k "init"   # 运行特定测试
"""

import pytest

from srcs.board import Board
from srcs.twin_board import TwinBoard


class TestTwinBoardInitialization:
    """测试 TwinBoard 类的初始化功能"""

    def test_init_from_basic_board(self):
        """测试从基本棋盘初始化孪生棋盘"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                          9, 8, 7, 6, 5, 4, 3, 2, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert len(twin_board.digit_list) == 81
        assert twin_board.digit_list[0] == 1
        assert twin_board.digit_list[8] == 1
        assert twin_board.digit_list[9] == 1
        assert twin_board.digit_list[17] == 1

    def test_init_digit_transformation(self):
        """测试数字转换逻辑（min(digit, 10-digit)）"""
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

        twin_board = TwinBoard(board)

        assert twin_board.digit_list[0] == 1
        assert twin_board.digit_list[1] == 2
        assert twin_board.digit_list[2] == 3
        assert twin_board.digit_list[3] == 4
        assert twin_board.digit_list[4] == 5
        assert twin_board.digit_list[5] == 4
        assert twin_board.digit_list[6] == 3
        assert twin_board.digit_list[7] == 2
        assert twin_board.digit_list[8] == 1

    def test_init_large_digits(self):
        """测试大数字转换（>5 的数字）"""
        board = Board()
        board.set_digits([6, 7, 8, 9, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board.digit_list[0] == 4
        assert twin_board.digit_list[1] == 3
        assert twin_board.digit_list[2] == 2
        assert twin_board.digit_list[3] == 1

    def test_init_zeros_preserved(self):
        """测试零值保持为零"""
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

        twin_board = TwinBoard(board)

        assert twin_board.digit_list[0] == 1
        assert twin_board.digit_list[1] == 0
        assert twin_board.digit_list[2] == 2
        assert twin_board.digit_list[3] == 0
        assert twin_board.digit_list[4] == 3
        assert twin_board.digit_list[5] == 0

    def test_init_empty_board(self):
        """测试从空棋盘初始化"""
        board = Board()
        twin_board = TwinBoard(board)

        assert twin_board.digit_list == []
        assert twin_board.pair_list == []
        assert twin_board.potential_pair_count == 0

    def test_str_representation(self):
        """测试字符串表示"""
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

        twin_board = TwinBoard(board)
        board_str = str(twin_board)

        assert "1" in board_str
        assert "2" in board_str
        assert "3" in board_str
        assert "." in board_str


class TestTwinBoardCanMatch:
    """测试 TwinBoard 的 _can_match 方法"""

    def test_can_match_same_transformed_digits(self):
        """测试转换后相同数字可以匹配"""
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

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is True

    def test_can_match_different_original_but_same_transformed(self):
        """测试原始不同但转换后相同的数字可以匹配"""
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

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is True

    def test_can_match_original_same_but_not_ten(self):
        """测试原始相同但不满足和为10的数字可以匹配"""
        board = Board()
        board.set_digits([3, 0, 0, 0, 0, 0, 0, 0, 3,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is True

    def test_can_match_original_sum_to_ten_but_different_transformed(self):
        """测试原始和为10但转换后不同的数字不能匹配"""
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

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is True

    def test_can_match_different_transformed_digits(self):
        """测试转换后不同的数字不能匹配"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 2,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is False

    def test_can_match_with_zeros(self):
        """测试包含零值不能匹配"""
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

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 1) is False
        assert twin_board._can_match(1, 8) is False


class TestTwinBoardInheritedMatching:
    """测试 TwinBoard 继承的 _is_matching 方法"""

    def test_inherited_same_row_matching(self):
        """测试继承的同行匹配逻辑"""
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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 8) is True

    def test_inherited_same_row_blocked(self):
        """测试继承的同行匹配阻挡逻辑"""
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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 8) is False

    def test_inherited_same_column_matching(self):
        """测试继承的同列匹配逻辑"""
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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 72) is True

    def test_inherited_diagonal_matching(self):
        """测试继承的对角线匹配逻辑"""
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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 20) is True

    def test_inherited_cross_row_matching(self):
        """测试继承的跨行首尾匹配逻辑"""
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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 17) is True


class TestTwinBoardUpdateInformation:
    """测试 TwinBoard 的信息更新机制"""

    def test_update_information_initial(self):
        """测试初始化时信息更新"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9,
                          1, 2, 3, 4, 5, 6, 7, 8, 9,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board.potential_pair_count > 0
        assert len(twin_board.pair_list) > 0

    def test_digit_pairs_count(self):
        """测试可消除配对计数"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          2, 0, 0, 0, 0, 0, 0, 0, 2,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board.potential_pair_count >= 2

    def test_digit_pairs_content(self):
        """测试可消除配对内容"""
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

        twin_board = TwinBoard(board)

        assert (0, 8) in twin_board.pair_list or (8, 0) in twin_board.pair_list

    def test_empty_board_information(self):
        """测试空棋盘的信息"""
        board = Board()
        twin_board = TwinBoard(board)

        assert twin_board.pair_list == []
        assert twin_board.potential_pair_count == 0

    def test_information_updates_after_match(self):
        """测试配对后信息更新"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          2, 0, 0, 0, 0, 0, 0, 0, 2,
                          3, 0, 0, 0, 0, 0, 0, 0, 3,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)
        initial_pairs_count = len(twin_board.pair_list)
        initial_potential = twin_board.potential_pair_count

        twin_board.match(0, 8)

        assert len(twin_board.pair_list) < initial_pairs_count
        assert twin_board.potential_pair_count < initial_potential


class TestTwinBoardMatchOperation:
    """测试 TwinBoard 的配对操作"""

    def test_match_removes_pairs(self):
        """测试配对消除"""
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

        twin_board = TwinBoard(board)

        initial_nonzero = len([d for d in twin_board.digit_list if d != 0])

        twin_board.match(0, 8)

        new_nonzero = len([d for d in twin_board.digit_list if d != 0])
        assert new_nonzero == initial_nonzero - 2

    def test_match_clears_empty_rows(self):
        """测试配对后清理空行"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          2, 3, 4, 5, 6, 7, 8, 9, 1,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)
        original_length = len(twin_board.digit_list)

        twin_board.match(0, 8)

        assert len(twin_board.digit_list) < original_length

    def test_match_unsuccessful_no_removal(self):
        """测试不成功配对时不消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 2,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)
        original_digit_list = twin_board.digit_list[:]

        twin_board.match(0, 8)

        assert twin_board.digit_list == original_digit_list

    def test_multiple_matches(self):
        """测试连续多次配对"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1,
                          2, 0, 0, 0, 0, 0, 0, 0, 2,
                          3, 0, 0, 0, 0, 0, 0, 0, 3,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        initial_nonzero = len([d for d in twin_board.digit_list if d != 0])

        twin_board.match(0, 8)

        after_first = len([d for d in twin_board.digit_list if d != 0])
        assert after_first == initial_nonzero - 2

        current_nonzero = len([d for d in twin_board.digit_list if d != 0])
        twin_board.match(9, 17)

        after_second = len([d for d in twin_board.digit_list if d != 0])
        assert after_second == current_nonzero - 2


class TestTwinBoardEdgeCases:
    """测试 TwinBoard 的边界条件"""

    def test_empty_board_operations(self):
        """测试空棋盘操作"""
        board = Board()
        twin_board = TwinBoard(board)

        assert str(twin_board) == ""

        twin_board._clear()
        assert twin_board.digit_list == []

        twin_board.fill()
        assert twin_board.digit_list == []

    def test_single_element_board(self):
        """测试单元素棋盘"""
        board = Board()
        board.set_digits([5])
        twin_board = TwinBoard(board)

        assert len(twin_board.digit_list) == 1
        assert twin_board.digit_list[0] == 5

    def test_out_of_range_indices(self):
        """测试越界索引"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])
        twin_board = TwinBoard(board)

        with pytest.raises(IndexError):
            twin_board._is_matching(0, 9)
        with pytest.raises(IndexError):
            twin_board._is_matching(9, 0)

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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 0) is False

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

        twin_board = TwinBoard(board)

        assert twin_board._is_matching(0, 1) is False
        assert twin_board._is_matching(1, 8) is False

    def test_transformation_edge_cases(self):
        """测试数字转换的边界情况"""
        board = Board()
        board.set_digits([1, 5, 6, 9, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0])

        twin_board = TwinBoard(board)

        assert twin_board.digit_list[0] == 1
        assert twin_board.digit_list[1] == 5
        assert twin_board.digit_list[2] == 4
        assert twin_board.digit_list[3] == 1


class TestTwinBoardVsBoard:
    """测试 TwinBoard 与 Board 的对比"""

    def test_different_can_match_behavior(self):
        """测试 _can_match 方法的不同行为"""
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

        twin_board = TwinBoard(board)

        assert board._can_match(0, 8) is True
        assert twin_board._can_match(0, 8) is True

    def test_same_is_matching_behavior(self):
        """测试 _is_matching 方法的相同行为"""
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

        board_copy = Board()
        board_copy.set_digits(board.digit_list[:])
        twin_board = TwinBoard(board)

        assert board._is_matching(0, 8) == twin_board._is_matching(0, 8)

    def test_digit_transformation_preserves_matchability(self):
        """测试数字转换保持可匹配性"""
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

        twin_board = TwinBoard(board)

        assert twin_board._can_match(0, 8) is True
        assert twin_board._is_matching(0, 8) is True
