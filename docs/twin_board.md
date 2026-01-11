# TwinBoard 类功能说明文档

## 类概述

**模块：** `srcs.twin_board`

**类名：** `TwinBoard`

**继承关系：** `TwinBoard` 继承自 `Board`

**设计目的：** `TwinBoard` 类是 NumberMatch（数字配对）游戏的辅助分析工具，用于计算当前局面的最优配对方案。该类将原始棋盘的数字转换为互补数表示（每个数字转换为
`min(digit, 10 - digit)`），从而将配对问题简化为"数值相等即可配对"的形式，便于搜索和计算所有可行的配对方案。

**核心特性：**

- 将数字转换为互补数表示（如 3 转换为 3，8 转换为 2）
- 自动计算所有可达的配对位置对
- 统计满足数字匹配条件的配对数量

## 属性说明

### `digit_list`

- **类型：** `list[int]`
- **说明：** 存储棋盘所有数字的一维列表。与父类 `Board` 不同，`TwinBoard` 中的数字是原始数字的互补数表示。列表长度为
  `9 × 行数`，每个元素为整数：
    - `0` 表示该格子为空（无数字）
    - `1-5` 表示该格子存放的互补数字
- **转换规则：** `digit_list[i] = min(original_digit, 10 - original_digit)`（当 original_digit != 0 时）
- **示例：** 原始数字 `[1, 5, 3, 9, 2, 8, 4, 6, 7]` 转换为 `[1, 5, 3, 1, 2, 2, 4, 4, 3]`

### `digit_pairs`

- **类型：** `list[tuple[int, int]]`
- **说明：** 存储所有可达配对的位置对列表。每个元素是一个元组，包含两个全局索引，表示这两个位置可以配对消除。
- **更新时机：** 在 `__init__` 和 `match` 方法中通过 `_update_information()` 自动更新
- **示例：** `[(0, 3), (1, 8), (4, 5)]` 表示索引 0 和 3 可配对，索引 1 和 8 可配对，索引 4 和 5 可配对

### `potential_num`

- **类型：** `int`
- **说明：** 统计所有满足数字匹配条件的配对数量。与 `digit_pairs` 不同，此属性包含所有满足数字匹配（互补数相等）但可能不满足路径可达条件的配对。
- **更新时机：** 在 `__init__` 和 `match` 方法中通过 `_update_information()` 自动更新（实际在 `_update_information()`
  内部初始化为 0 后累加）

## 方法说明

### `__init__`

```python
def __init__(self, board: Board)
```

**功能描述：** 初始化 `TwinBoard` 实例。通过接收一个 `Board` 实例，将其数字列表转换为互补数表示，并计算初始的配对信息。

**参数：**

| 参数名     | 类型      | 说明           |
|---------|---------|--------------|
| `board` | `Board` | 原始的 Board 实例 |

**返回值：** 无

**使用示例：**

```python
from board import Board
from twin_board import TwinBoard

# 创建原始棋盘
board = Board()
board.set_digits([1, 5, 3, 9, 2, 8, 4, 6, 7])

# 创建孪生棋盘
twin_board = TwinBoard(board)
# digit_list 变为 [1, 5, 3, 1, 2, 2, 4, 4, 3]
```

---

### `__str__`

```python
def __str__(self) -> str
```

**功能描述：** 返回棋盘的可视化字符串表示。使用 `.` 字符代替 0 显示空格，数字正常显示，每行 9 个元素，以换行符分隔。

**参数：** 无

**返回值：** `str` - 棋盘的可视化字符串表示

**使用示例：**

```python
twin_board = TwinBoard(board)
print(twin_board)
# 输出（互补数表示）：
# 1 5 3 1 2 2 4 4 3
```

**注意：** 此方法继承自 `Board` 类。

---

### `set_digits`

```python
def set_digits(self, digit_list: list[int]) -> None
```

**功能描述：** 设置棋盘的当前局面。直接用提供的数字列表替换现有的 `digit_list`。

**参数：**

| 参数名          | 类型          | 说明                  |
|--------------|-------------|---------------------|
| `digit_list` | `list[int]` | 表示局面的整数列表，使用 0 表示空格 |

**返回值：** `None`

**使用示例：**

```python
twin_board = TwinBoard(board)
twin_board.set_digits([1, 2, 3, 4, 5, 0, 0, 0, 0])
```

**注意：** 此方法继承自 `Board` 类，但通常不直接使用，建议通过 `__init__` 接收 `Board` 实例来初始化。

---

### `_update_information`

```python
def _update_information(self) -> None
```

**功能描述：** 更新配对信息。重新计算 `digit_pairs`（可达配对列表）和 `potential_num`（潜在配对数量）。

**计算逻辑：**

1. 清空 `digit_pairs` 列表和 `potential_num` 计数器
2. 遍历所有位置对 `(i, j)`（其中 `i < j`）：
    - 如果 `_can_match(i, j)` 为 `True`，则 `potential_num` 增加 1
    - 如果 `_is_matching(i, j)` 为 `True`，则将 `(i, j)` 添加到 `digit_pairs`

**参数：** 无

**返回值：** `None`

**使用示例：**

```python
twin_board = TwinBoard(board)
twin_board.match(0, 8)  # 配对消除后
twin_board._analyze()  # 手动更新配对信息
print(twin_board.pair_list)  # 查看可达配对列表
print(twin_board.potential_pair_count)  # 查看潜在配对数量
```

---

### `_can_match`

```python
def _can_match(self, global_index1: int, global_index2: int) -> bool
```

**功能描述：** 判断两个位置的数字是否满足配对条件。与父类 `Board` 的 `_can_match` 方法不同，`TwinBoard`
仅检查数值是否相等（因为互补数表示已将"和为10"的情况转化为"数值相等"）。

**数字匹配规则：** 两个数字可以配对的前提条件为数值相同。

**参数：**

| 参数名             | 类型    | 说明                  |
|-----------------|-------|---------------------|
| `global_index1` | `int` | 第一个位置的全局索引（0-based） |
| `global_index2` | `int` | 第二个位置的全局索引（0-based） |

**返回值：** `bool` - 如果两个数字满足配对条件则返回 `True`，否则返回 `False`

**使用示例：**

```python
twin_board = TwinBoard(board)

# 互补数相等
print(twin_board._can_match(0, 3))  # True（两个 1）
print(twin_board._can_match(1, 8))  # False（5 和 3 不等，无法配对）

# 互补数不等
print(twin_board._can_match(0, 1))  # False（1 和 5 不等）
```

---

### `_is_matching`

```python
def _is_matching(self, global_index1: int, global_index2: int) -> bool
```

**功能描述：** 判断两个位置是否满足配对条件。首先检查两个数字是否满足 `_can_match` 条件，然后检查两个位置之间是否存在有效的配对路径。

**配对条件（需同时满足）：**

1. **数字匹配条件**（由 `_can_match` 判断）：
    - 两个位置的互补数必须相等
2. **路径可达条件**：
    - 两个位置之间必须没有其他非空数字
    - 配对路径必须满足以下任一条件：
        - 相同行（水平相邻或间隔一至多格）
        - 相同列（垂直相邻或间隔一至多格）
        - 对角线相邻
        - 跨行首尾相邻（两行首尾位置的数字可配对）

**参数：**

| 参数名             | 类型    | 说明                  |
|-----------------|-------|---------------------|
| `global_index1` | `int` | 第一个位置的全局索引（0-based） |
| `global_index2` | `int` | 第二个位置的全局索引（0-based） |

**返回值：** `bool` - 如果两个位置能够配对消除则返回 `True`，否则返回 `False`

**配对规则详解：**

| 规则类型 | 条件                                                          | 说明                    |
|------|-------------------------------------------------------------|-----------------------|
| 相同行  | `row_index1 == row_index2`                                  | 同一行内，两个位置之间必须全为空格     |
| 相同列  | `col_index1 == col_index2`                                  | 同一列内，两个位置之间必须全为空格     |
| 对角线  | `row1 + col1 == row2 + col2` 或 `row1 - row2 == col1 - col2` | 同对角线内，两位置之间必须全为空格     |
| 跨行首尾 | `abs(row1 - row2) == 1`                                     | 相邻两行，按索引顺序两位置之间必须全为空格 |

**使用示例：**

```python
board = Board()
board.set_digits([1, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 1])
twin_board = TwinBoard(board)

# 相同行配对（1 和 1 互补数都是 1）
print(twin_board._is_pair(0, 8))  # True

# 跨行首尾配对（9 转换为 1，1 还是 1）
print(twin_board._is_pair(0, 17))  # True
```

**注意：** 此方法继承自 `Board` 类。

---

### `_clear`

```python
def _clear(self) -> None
```

**功能描述：** 清理棋盘中的空行。将全为 0 的行从棋盘中移除，保留非空行，并将所有剩余数字压缩到顶部。

**参数：** 无

**返回值：** `None`

**使用示例：**

```python
twin_board.set_digits([1, 2, 3, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0,
                       4, 5, 6, 0, 0, 0, 0, 0, 0])
twin_board._clear()
# _clear 后 digit_list 变为 [1, 2, 3, 4, 5, 6]
```

**注意：** 此方法继承自 `Board` 类，通常在 `match()` 操作后自动调用。

---

### `fill`

```python
def fill(self) -> None
```

**功能描述：** 拷贝填充。将棋盘中剩余的非空数字复制到列表末尾，实现数字的填充和重排。

**参数：** 无

**返回值：** `None`

**使用示例：**

```python
twin_board.set_digits([1, 2, 0, 3, 0])
twin_board.fill()  # 填充后 digit_list 为 [1, 2, 3, 0, 0, 1, 2, 3, 0]
```

**注意：** 此方法继承自 `Board` 类。

---

### `match`

```python
def match(self, global_index1: int, global_index2: int) -> None
```

**功能描述：** 执行配对消除操作。首先调用父类 `Board` 的 `match` 方法执行配对消除和清理空行，然后调用
`_update_information()` 更新配对信息。

**参数：**

| 参数名             | 类型    | 说明                  |
|-----------------|-------|---------------------|
| `global_index1` | `int` | 第一个位置的全局索引（0-based） |
| `global_index2` | `int` | 第二个位置的全局索引（0-based） |

**返回值：** `None`

**使用示例：**

```python
board = Board()
board.set_digits([1, 2, 3, 4, 5, 6, 7, 8, 9])
twin_board = TwinBoard(board)

# 1 和 9 和为 10，转换为互补数后都是 1，可以配对
twin_board.match(0, 8)
print(twin_board.digit_list)  # [0, 2, 3, 4, 5, 6, 7, 8, 0]
print(twin_board.pair_list)  # 更新后的可达配对列表
```

---

## 互补数转换详解

### 转换原理

`TwinBoard` 将每个数字 `d` 转换为 `min(d, 10 - d)`，这一转换基于以下观察：

- 如果两个数字之和为 10，则它们的互补数相等
- 例如：3 和 7 → min(3, 7) = 3 和 min(7, 3) = 3

### 转换对照表

| 原始数字 | 互补数 |
|------|-----|
| 1    | 1   |
| 2    | 2   |
| 3    | 3   |
| 4    | 4   |
| 5    | 5   |
| 6    | 4   |
| 7    | 3   |
| 8    | 2   |
| 9    | 1   |

### 配对规则简化

通过互补数转换，NumberMatch 游戏的配对规则从"数值相同或和为 10"简化为"数值相同"：

| 原始规则           | 互补数规则         |
|----------------|---------------|
| 数值相同（如 5 和 5）  | 数值相同（如 5 和 5） |
| 和为 10（如 3 和 7） | 数值相同（如 3 和 3） |
| 无法配对（如 3 和 6）  | 无法配对（如 3 和 4） |

## 方法访问级别说明

本类中的方法按照访问级别分为以下几类：

| 方法名                                                          | 访问级别 | 说明                      |
|--------------------------------------------------------------|------|-------------------------|
| `__init__`, `__str__`                                        | 特殊方法 | Python 特殊方法，用于初始化和字符串表示 |
| `set_digits`, `match`, `fill`                                | 公开   | 公开接口，供外部代码调用            |
| `_can_match`, `_is_matching`, `_clear`,`_update_information` | 私有   | 内部实现细节，主要供类内部方法使用       |

**设计原则：** `TwinBoard` 类通过互补数转换简化配对判断逻辑，同时保持与 `Board` 类一致的接口设计，便于集成到现有游戏架构中。

## 注意事项

1. **互补数转换的不可逆性：** 一旦数字被转换为互补数形式，就无法直接恢复原始数字。必要时应在操作前保存原始 Board 的状态。

2. **配对信息的自动更新：** `digit_pairs` 和 `potential_num` 在 `__init__` 和 `match()` 后会自动更新，但在直接调用
   `set_digits()` 后需要手动调用 `_update_information()` 以获取最新的配对信息。

3. **fill() 方法对配对信息的影响：** 调用 `fill()` 后，`digit_pairs` 和 `potential_num` 不会自动更新，需要手动调用
   `_update_information()` 以反映新的棋盘状态。
