import pytest
from srcs.board import Board


class TestBoardInit:
    """测试Board初始化"""

    def test_init_empty_board(self):
        """测试初始化空棋盘"""
        board = Board()
        assert board.digit_list == []

    def test_init_default_no_args(self):
        """测试不带参数的初始化"""
        board = Board()
        assert hasattr(board, 'digit_list')


class TestBoardStr:
    """测试Board字符串表示"""

    def test_str_empty_board(self):
        """测试空棋盘的字符串表示"""
        board = Board()
        board.set_digits([])
        result = str(board)
        assert result == ""

    def test_str_with_zeros(self):
        """测试包含空位的棋盘字符串表示"""
        board = Board()
        board.set_digits([1, 0, 0, 2, 0, 0, 3, 0, 0])
        result = str(board)
        assert '1 . .' in result
        assert '2 . .' in result
        assert '3 . .' in result

    def test_str_no_zeros(self):
        """测试不包含空位的棋盘字符串表示"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5])
        result = str(board)
        assert '1 2 3' in result
        assert '4 5' in result


class TestBoardSetDigits:
    """测试set_digits方法"""

    def test_set_empty_digits(self):
        """测试设置空数字列表"""
        board = Board()
        board.set_digits([])
        assert board.digit_list == []

    def test_set_single_digit(self):
        """测试设置单个数字"""
        board = Board()
        board.set_digits([5])
        assert board.digit_list == [5]

    def test_set_multiple_digits(self):
        """测试设置多个数字"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert len(board.digit_list) == 9

    def test_set_digits_with_zeros(self):
        """测试设置包含0的数字列表"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3])
        assert board.digit_list == [1, 0, 2, 0, 3]


class TestBoardMatch:
    """测试match方法"""

    def test_match_same_digit_same_row(self):
        """测试相同数字在同一行的消除"""
        board = Board()
        board.set_digits([1, 1])
        board.match(0, 1)
        assert board.digit_list == []

    def test_match_same_digit_same_column(self):
        """测试相同数字在同一列的消除"""
        board = Board()
        board.set_digits([1, 0, 0, 1, 0, 0, 0, 0, 0])
        board.match(0, 3)
        assert board.digit_list == []

    def test_match_same_digit_diagonal(self):
        """测试相同数字在对角线的消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1])
        board.match(0, 8)
        assert board.digit_list == []

    def test_match_sum_to_ten_same_row(self):
        """测试和为10在同一行的消除"""
        board = Board()
        board.set_digits([3, 7])
        board.match(0, 1)
        assert board.digit_list == []

    def test_match_sum_to_ten_same_column(self):
        """测试和为10在同一列的消除"""
        board = Board()
        board.set_digits([4, 0, 0, 6, 0, 0, 0, 0, 0])
        board.match(0, 3)
        assert board.digit_list == []

    def test_match_sum_to_ten_diagonal(self):
        """测试和为10在对角线的消除"""
        board = Board()
        board.set_digits([4, 0, 0, 0, 0, 0, 0, 0, 6])
        board.match(0, 8)
        assert board.digit_list == []

    def test_match_cross_row_edge(self):
        """测试跨行首尾的消除"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9, 1])
        initial_len = len(board.digit_list)
        board.match(0, 9)
        assert len(board.digit_list) < initial_len

    def test_match_no_match_different_digits(self):
        """测试不同数字无法消除"""
        board = Board()
        board.set_digits([1, 2, 0, 0, 0, 0, 0, 0, 0])
        board.match(0, 1)
        assert board.digit_list[0] == 1
        assert board.digit_list[1] == 2

    def test_match_blocked_same_row(self):
        """测试相同行中间有阻隔无法消除"""
        board = Board()
        board.set_digits([1, 2, 1, 0, 0, 0, 0, 0, 0])
        board.match(0, 2)
        assert board.digit_list[0] == 1
        assert board.digit_list[1] == 2
        assert board.digit_list[2] == 1

    def test_match_blocked_same_column(self):
        """测试相同列中间有阻隔无法消除"""
        board = Board()
        board.set_digits([1, 0, 0, 2, 0, 1, 0, 0, 0])
        board.match(0, 5)
        assert board.digit_list[0] == 1
        assert board.digit_list[3] == 2
        assert board.digit_list[5] == 1

    def test_match_blocked_diagonal(self):
        """测试对角线中间有阻隔无法消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 2, 0, 0, 0, 1])
        board.match(0, 8)
        assert board.digit_list[0] == 1
        assert board.digit_list[4] == 2
        assert board.digit_list[8] == 1

    def test_match_blocked_column_with_zeros(self):
        """测试相同列但中间有非零阻隔"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        board.match(0, 18)
        assert board.digit_list[0] == 1
        assert board.digit_list[9] == 2
        assert board.digit_list[18] == 1

    def test_match_diagonal_with_zeros_between(self):
        """测试对角线中间无阻隔"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1])
        assert board._is_pair(0, 8) is True

    def test_match_diagonal_with_non_zero_block(self):
        """测试对角线中间有非零阻隔"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 2, 0, 0, 0, 1])
        assert board._is_pair(0, 8) is False

    def test_match_with_zero(self):
        """测试包含0无法消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0])
        board.match(0, 1)
        assert board.digit_list[0] == 1
        assert board.digit_list[1] == 0

    def test_match_same_index(self):
        """测试相同索引无法消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0])
        board.match(0, 0)
        assert board.digit_list[0] == 1

    def test_match_unrelated_positions(self):
        """测试不相关位置无法消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        original_digits = board.digit_list.copy()
        board.match(0, 17)
        assert board.digit_list[0] == 1
        assert board.digit_list[17] == 1
        assert board.digit_list == original_digits

    def test_match_anti_diagonal(self):
        """测试反对角线消除"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 1])
        board.match(0, 8)
        assert board.digit_list == []

    def test_match_multi_row_cross(self):
        """测试多行跨行首尾消除"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        board.match(0, 9)
        assert board.digit_list[0] == 0

    def test_match_anti_diagonal_with_block(self):
        """测试反对角线中间有阻隔"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 2, 0, 0, 0, 1])
        board.match(0, 8)
        assert board.digit_list[0] == 1
        assert board.digit_list[4] == 2
        assert board.digit_list[8] == 1

    def test_match_diagonal_blocked_in_middle(self):
        """测试对角线中间有非零阻隔无法消除（第84-85行）"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
        original_digits = board.digit_list[:]
        board.match(4, 20)
        assert board.digit_list == original_digits

    def test_match_unrelated_positions_full(self):
        """测试完全不相关的位置无法消除（第97行）"""
        board = Board()
        board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
        original_digits = board.digit_list[:]
        board.match(0, 19)
        assert board.digit_list == original_digits

    def test_match_clear_after_elimination(self):
        """测试消除后自动清理空行"""
        board = Board()
        board.set_digits([1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2])
        board.match(0, 1)
        board.match(0, 1)
        assert 0 not in board.digit_list


class TestBoardFill:
    """测试fill方法"""

    def test_fill_empty_board(self):
        """测试空棋盘填充"""
        board = Board()
        board.set_digits([])
        board.fill()
        assert board.digit_list == []

    def test_fill_with_zeros(self):
        """测试带空位的棋盘填充"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3, 0])
        board.fill()
        assert board.digit_list == [1, 0, 2, 0, 3, 0, 1, 2, 3]

    def test_fill_no_zeros(self):
        """测试无空位的棋盘填充"""
        board = Board()
        board.set_digits([1, 2, 3])
        board.fill()
        assert board.digit_list == [1, 2, 3, 1, 2, 3]

    def test_fill_partial_zeros(self):
        """测试部分空位的棋盘填充"""
        board = Board()
        board.set_digits([1, 0, 0, 2, 3])
        board.fill()
        assert board.digit_list == [1, 0, 0, 2, 3, 1, 2, 3]


class TestBoardClear:
    """测试清理功能"""

    def test_clear_empty_rows(self):
        """测试清理空行"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 0])
        board._clear()
        assert board.digit_list == []

    def test_clear_partial_empty(self):
        """测试部分行为空的清理"""
        board = Board()
        board.set_digits([0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 6])
        board._clear()
        assert board.digit_list == [4, 5, 6]


class TestBoardIntegration:
    """测试Board综合场景"""

    def test_complex_match_sequence(self):
        """测试复杂消除序列"""
        board = Board()
        board.set_digits([1, 9, 2, 8, 3, 7, 4, 6, 5, 5, 6, 4, 7, 3, 8, 2, 9, 1])
        board.match(0, 1)
        assert board.digit_list[0] == 0
        assert board.digit_list[1] == 0
        board.match(2, 3)
        assert board.digit_list[2] == 0
        assert board.digit_list[3] == 0

    def test_multi_digit_board(self):
        """测试多行棋盘"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 8, 7, 6, 5, 4, 3, 2, 1])
        result = str(board)
        lines = result.split('\n')
        assert len(lines) == 2

    def test_empty_after_all_match(self):
        """测试全部消除后为空"""
        board = Board()
        board.set_digits([5, 5, 6, 4, 7, 3])
        board.match(0, 1)
        board.match(2, 3)
        board.match(4, 5)
        assert board.digit_list == []
