# NumberMatch 术语表

## 核心术语

| 术语        | 描述               |
|-----------|------------------|
| **clear** | 棋盘操作（被动） —— 清理空行 |
| **match** | 棋盘操作（主动） —— 配对消除 |
| **fill**  | 棋盘操作（主动） —— 拷贝填充 |

## 棋盘

| 术语                              | 描述              |
|---------------------------------|-----------------|
| **Board**                       | 类 —— 棋盘         |
| **.size**                       | 属性 —— 棋盘尺寸      |
| **.grid**                       | 属性 —— 棋盘网格      |
| **.calc_coord()**               | 方法（静态） —— 计算坐标  |
| **.set_grid()**                 | 方法 —— 设置局面      |
| **.generate_grid()**            | 方法 —— 生成局面      |
| **.get_digit_by_coord()**       | 方法 —— 按坐标获取数字   |
| **.get_digit_by_index()**       | 方法 —— 按索引获取数字   |
| **.set_digit_by_coord()**       | 方法 —— 按坐标设置数字   |
| **.set_digit_by_index()**       | 方法 —— 按索引设置数字   |
| **.is_matching()**              | 方法 —— 是否配对      |
| **.find_digit_pair()**          | 方法 —— 寻找有效数字对   |
| **.get_remaining_digits()**     | 方法 —— 获取剩余数字列表  |
| **.get_remaining_digits_num()** | 方法 —— 获取剩余数字数量  |
| **.get_remaining_rows_num()**   | 方法 —— 获取剩余有效行数量 |
| **.safe_copy()**                | 方法 —— 安全拷贝      |

## 边缘术语

| 术语               | 描述            |
|------------------|---------------|
| **digit**        | 数字            |
| **digit_pair**   | 有效数字对         |
| **coord**        | 坐标            |
| **global_index** | 全局索引（0-based） |
| **row_index**    | 行索引（0-based）  |
| **col_index**    | 列索引（0-based）  |
| **replica**      | 副本            |