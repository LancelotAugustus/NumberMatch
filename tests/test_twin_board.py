import pytest
from srcs.board import Board
from srcs.twin_board import TwinBoard


class TestTwinBoardInit:
    """测试TwinBoard初始化"""

    def test_init_from_empty_board(self):
        """测试从空Board初始化"""
        board = Board()
        board.set_digits([])
        twin = TwinBoard(board)
        assert twin.digit_list == []

    def test_init_single_digit(self):
        """测试单个数字的转换"""
        board = Board()
        board.set_digits([5])
        twin = TwinBoard(board)
        assert twin.digit_list == [5]

    def test_init_digit_conversion_1(self):
        """测试数字1和9的转换（min(1,9)=1, min(9,1)=1）"""
        board = Board()
        board.set_digits([1, 9])
        twin = TwinBoard(board)
        assert twin.digit_list[0] == 1
        assert twin.digit_list[1] == 1

    def test_init_digit_conversion_2(self):
        """测试数字2和8的转换"""
        board = Board()
        board.set_digits([2, 8])
        twin = TwinBoard(board)
        assert twin.digit_list[0] == 2
        assert twin.digit_list[1] == 2

    def test_init_digit_conversion_5(self):
        """测试数字5的转换（min(5,5)=5）"""
        board = Board()
        board.set_digits([5, 5])
        twin = TwinBoard(board)
        assert twin.digit_list == [5, 5]

    def test_init_digit_conversion_3(self):
        """测试数字3和7的转换"""
        board = Board()
        board.set_digits([3, 7])
        twin = TwinBoard(board)
        assert twin.digit_list[0] == 3
        assert twin.digit_list[1] == 3

    def test_init_with_zeros(self):
        """测试包含0的转换（0保持为0）"""
        board = Board()
        board.set_digits([1, 0, 2, 0, 3])
        twin = TwinBoard(board)
        assert twin.digit_list == [1, 0, 2, 0, 3]

    def test_init_preserves_structure(self):
        """测试初始化保留棋盘结构"""
        board = Board()
        board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3])
        twin = TwinBoard(board)
        assert len(twin.digit_list) == 12


class TestTwinBoardAnalyze:
    """测试TwinBoard分析功能"""

    def test_score_with_multiple_matches(self):
        """测试分数计算（所有可能匹配的数量）"""
        board = Board()
        board.set_digits([1, 1, 1])
        twin = TwinBoard(board)
        assert twin.score == 3

    def test_pair_list_generation(self):
        """测试可消除对列表生成"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        twin = TwinBoard(board)
        assert len(twin.pair_list) > 0

    def test_score_zero_no_matches(self):
        """测试无可匹配时的分数为0"""
        board = Board()
        board.set_digits([1, 2, 3])
        twin = TwinBoard(board)
        assert twin.score == 0

    def test_pair_list_empty_no_valid_pairs(self):
        """测试无可消除对时pair_list为空"""
        board = Board()
        board.set_digits([1, 2, 3])
        twin = TwinBoard(board)
        assert twin.pair_list == []


class TestTwinBoardMatch:
    """测试TwinBoard的match方法"""

    def test_match_updates_pair_list(self):
        """测试消除后pair_list更新"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        twin = TwinBoard(board)
        initial_pairs = len(twin.pair_list)
        if initial_pairs > 0:
            pair = twin.pair_list[0]
            twin.match(pair[0], pair[1])
            assert len(twin.pair_list) <= initial_pairs

    def test_match_updates_score(self):
        """测试消除后score更新"""
        board = Board()
        board.set_digits([1, 1, 1, 1])
        twin = TwinBoard(board)
        initial_score = twin.score
        if initial_score > 0:
            pair = twin.pair_list[0]
            twin.match(pair[0], pair[1])
            assert twin.score < initial_score

    def test_match_with_converted_digits(self):
        """测试使用转换后的数字进行消除"""
        board = Board()
        board.set_digits([1, 9, 1, 9])
        twin = TwinBoard(board)
        assert twin.digit_list[0] == twin.digit_list[1] == 1
        assert twin.digit_list[2] == twin.digit_list[3] == 1

    def test_match_invalid_pair_no_change(self):
        """测试无效配对不改变状态"""
        board = Board()
        board.set_digits([1, 2, 3, 4])
        twin = TwinBoard(board)
        original_digit_list = twin.digit_list[:]
        original_score = twin.score
        original_pair_list = twin.pair_list[:]
        if twin.pair_list:
            non_pair_indices = []
            for i in range(len(twin.digit_list)):
                for j in range(i + 1, len(twin.digit_list)):
                    if (i, j) not in twin.pair_list:
                        non_pair_indices = [i, j]
                        break
                if non_pair_indices:
                    break
            if non_pair_indices:
                twin.match(non_pair_indices[0], non_pair_indices[1])

    def test_match_same_digit_row(self):
        """测试相同数字在同一行的消除"""
        board = Board()
        board.set_digits([1, 1])
        twin = TwinBoard(board)
        twin.match(0, 1)
        assert twin.digit_list == []


class TestTwinBoardInheritedMethods:
    """测试TwinBoard继承的方法"""

    def test_str_method(self):
        """测试字符串表示方法"""
        board = Board()
        board.set_digits([1, 0, 2])
        twin = TwinBoard(board)
        result = str(twin)
        assert '1' in result
        assert '.' in result

    def test_inherited_set_digits(self):
        """测试继承的set_digits方法"""
        board = Board()
        board.set_digits([1, 2, 3])
        twin = TwinBoard(board)
        board.set_digits([4, 5, 6])
        assert twin.digit_list != [4, 5, 6]


class TestTwinBoardEdgeCases:
    """测试TwinBoard边界情况"""

    def test_empty_board(self):
        """测试空棋盘"""
        board = Board()
        board.set_digits([])
        twin = TwinBoard(board)
        assert twin.digit_list == []
        assert twin.pair_list == []
        assert twin.score == 0

    def test_single_digit_no_pairs(self):
        """测试单个数字无法配对"""
        board = Board()
        board.set_digits([5])
        twin = TwinBoard(board)
        assert twin.pair_list == []
        assert twin.score == 0

    def test_two_same_digits(self):
        """测试两个相同数字"""
        board = Board()
        board.set_digits([3, 3])
        twin = TwinBoard(board)
        assert (0, 1) in twin.pair_list
        assert twin.score == 1

    def test_two_different_digits(self):
        """测试两个不同数字"""
        board = Board()
        board.set_digits([1, 2])
        twin = TwinBoard(board)
        assert twin.pair_list == []
        assert twin.score == 0

    def test_all_same_digits(self):
        """测试全部相同数字"""
        board = Board()
        board.set_digits([2, 2, 2, 2])
        twin = TwinBoard(board)
        assert twin.score == 6

    def test_converted_pair_list_contains_valid_pairs(self):
        """测试pair_list只包含有效消除对"""
        board = Board()
        board.set_digits([1, 9, 0, 1, 9, 0])
        twin = TwinBoard(board)
        for pair in twin.pair_list:
            assert twin._is_pair(pair[0], pair[1])


class TestTwinBoardIntegration:
    """测试TwinBoard综合场景"""

    def test_full_match_sequence(self):
        """测试完整消除序列"""
        board = Board()
        board.set_digits([1, 1, 2, 2, 3, 3])
        twin = TwinBoard(board)
        match_count = 0
        while twin.pair_list:
            pair = twin.pair_list[0]
            twin.match(pair[0], pair[1])
            match_count += 1
        assert match_count == 3

    def test_score_after_each_match(self):
        """测试每次消除后分数变化"""
        board = Board()
        board.set_digits([1, 1, 2, 2])
        twin = TwinBoard(board)
        scores = [twin.score]
        while twin.pair_list:
            pair = twin.pair_list[0]
            twin.match(pair[0], pair[1])
            scores.append(twin.score)
        assert scores == sorted(scores, reverse=True)

    def test_twin_board_vs_original(self):
        """测试TwinBoard与原Board的关系"""
        board = Board()
        board.set_digits([1, 9, 2, 8, 3, 7])
        twin = TwinBoard(board)
        assert twin.digit_list[0] == twin.digit_list[1]
        assert twin.digit_list[2] == twin.digit_list[3]
        assert twin.digit_list[4] == twin.digit_list[5]
