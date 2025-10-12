# Python 数据类型详解

# Python 数据类型详解

# Python 的数据类型可以分为三大类：基本数据类型、复合数据类型和特殊数据类型

# ========================== 基本数据类型 ==========================

# 1. 整数 (int)
# 表示任意大小的整数，Python 3中的整数没有大小限制，可以处理非常大的整数
integer_example = 100  # 十进制整数
binary_integer = 0b1100100  # 二进制整数（以0b开头）
octal_integer = 0o144  # 八进制整数（以0o开头）
hex_integer = 0x64  # 十六进制整数（以0x开头）
large_integer = 10**100  # Python支持任意大的整数（也称为大数）
negative_integer = -42  # 负整数

print(f"十进制整数: {integer_example}")
print(f"二进制整数(0b1100100): {binary_integer}")
print(f"八进制整数(0o144): {octal_integer}")
print(f"十六进制整数(0x64): {hex_integer}")
print(f"整数类型: {type(integer_example)}")
print(f"大整数示例: {large_integer}")
print(f"负整数示例: {negative_integer}")

# 整数转换
# 将其他进制的字符串转换为整数
bin_str = "1100100"
int_from_bin = int(bin_str, 2)  # 从二进制字符串转换

hex_str = "64"
int_from_hex = int(hex_str, 16)  # 从十六进制字符串转换

print(f"从二进制字符串'{bin_str}'转换为整数: {int_from_bin}")
print(f"从十六进制字符串'{hex_str}'转换为整数: {int_from_hex}")

# 整数运算
# 基本算术运算
a = 10
b = 3

print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"除法: {a} / {b} = {a / b}")  # 结果为浮点数
print(f"整除: {a} // {b} = {a // b}")  # 向下取整
print(f"取余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# 位运算
c = 10  # 二进制: 1010
d = 3   # 二进制: 0011

print(f"按位与: {c} & {d} = {c & d}")  # 1010 & 0011 = 0010 (2)
print(f"按位或: {c} | {d} = {c | d}")  # 1010 | 0011 = 1011 (11)
print(f"按位异或: {c} ^ {d} = {c ^ d}")  # 1010 ^ 0011 = 1001 (9)
print(f"按位取反: ~{c} = {~c}")  # ~1010 = -(1010 + 1) = -11
print(f"左移: {c} << 2 = {c << 2}")  # 1010 << 2 = 101000 (40)
print(f"右移: {c} >> 2 = {c >> 2}")  # 1010 >> 2 = 10 (2)

# 比较运算
print(f"相等: {a} == {b} = {a == b}")
print(f"不相等: {a} != {b} = {a != b}")
print(f"大于: {a} > {b} = {a > b}")
print(f"小于: {a} < {b} = {a < b}")
print(f"大于等于: {a} >= {b} = {a >= b}")
print(f"小于等于: {a} <= {b} = {a <= b}")

# 整数的常用函数
print(f"绝对值: abs({negative_integer}) = {abs(negative_integer)}")
print(f"最大值: max({a}, {b}, {c}) = {max(a, b, c)}")
print(f"最小值: min({a}, {b}, {c}) = {min(a, b, c)}")
print(f"求和: sum([{a}, {b}, {c}]) = {sum([a, b, c])}")

# Python 3.8+ 的海象运算符 (:=) - 同时赋值和比较
# 以下代码仅在Python 3.8+ 可用
# if (n := a + b) > 10:
#     print(f"a + b = {n} > 10")

# 2. 浮点数 (float)
# 表示小数，Python中的浮点数遵循IEEE 754双精度标准（64位）
float_example = 3.14159  # 普通浮点数
scientific_notation = 2.5e-3  # 科学计数法，相当于0.0025
exponential_notation = 1.23e5  # 科学计数法，相当于123000
negative_float = -2.71828

print(f"浮点数示例: {float_example}")
print(f"科学计数法(2.5e-3): {scientific_notation}")
print(f"科学计数法(1.23e5): {exponential_notation}")
print(f"浮点数类型: {type(float_example)}")
print(f"负浮点数示例: {negative_float}")

# 整数和浮点数的转换
int_to_float = float(42)
float_to_int = int(3.999)  # 截断小数部分，结果为3
float_to_int_rounded = round(3.999)  # 四舍五入，结果为4

print(f"整数转浮点数: float(42) = {int_to_float}")
print(f"浮点数转整数(截断): int(3.999) = {float_to_int}")
print(f"浮点数转整数(四舍五入): round(3.999) = {float_to_int_rounded}")

# 浮点数运算
# 基本算术运算
a = 3.5
b = 2.1

print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"除法: {a} / {b} = {a / b}")
print(f"整除: {a} // {b} = {a // b}")  # 浮点数的整除结果仍为浮点数
print(f"取余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# 浮点数的精度问题
# 由于浮点数在计算机中是以二进制表示的，某些十进制小数无法精确表示
# 这会导致一些看似简单的计算结果不符合预期
precision_issue = 0.1 + 0.2
print(f"精度问题示例: 0.1 + 0.2 = {precision_issue}")
print(f"精度问题(格式化): 0.1 + 0.2 = {precision_issue:.15f}")

# 处理浮点数精度问题的方法
# 1. 使用round函数
rounded = round(0.1 + 0.2, 1)
print(f"使用round函数: round(0.1 + 0.2, 1) = {rounded}")

# 2. 使用decimal模块（更精确的十进制运算）
from decimal import Decimal, getcontext

getcontext().prec = 10
decimal_result = Decimal('0.1') + Decimal('0.2')
print(f"使用Decimal模块: Decimal('0.1') + Decimal('0.2') = {decimal_result}")

# 浮点数的特殊值
positive_infinity = float('inf')  # 正无穷大
negative_infinity = float('-inf')  # 负无穷大
not_a_number = float('nan')  # 非数字（Not a Number）

print(f"正无穷大: {positive_infinity}")
print(f"负无穷大: {negative_infinity}")
print(f"非数字: {not_a_number}")

# 检查特殊值
print(f"是否为无穷大: isinf({positive_infinity}) = {float('inf').isinf()}")
print(f"是否为非数字: isnan({not_a_number}) = {float('nan').isnan()}")

# 浮点数的常用函数
print(f"绝对值: abs({negative_float}) = {abs(negative_float)}")
print(f"最大值: max({a}, {b}, 4.2) = {max(a, b, 4.2)}")
print(f"最小值: min({a}, {b}, 0.5) = {min(a, b, 0.5)}")
print(f"平方根: sqrt(16.0) = {16.0 ** 0.5}")  # 使用幂运算计算平方根
print(f"四舍五入到指定小数位数: round({float_example}, 3) = {round(float_example, 3)}")

# 3. 复数 (complex)
# 表示复数，形式为 a + bj，其中 a 是实部，b 是虚部
complex_example = 3 + 4j  # 直接创建复数
another_complex = complex(2, 3)  # 使用complex()函数创建
negative_complex = -1 - 2j  # 负复数

print(f"复数示例: {complex_example}")
print(f"使用complex()函数创建: {another_complex}")
print(f"负复数示例: {negative_complex}")
print(f"复数类型: {type(complex_example)}")

# 访问复数的实部和虚部
real_part = complex_example.real
imaginary_part = complex_example.imag
print(f"实部: {real_part}, 虚部: {imaginary_part}")

# 访问复数的共轭
conjugate = complex_example.conjugate()
print(f"共轭复数: {conjugate}")  # 共轭复数的虚部符号取反

# 从字符串创建复数
complex_from_str = complex("1+2j")
print(f"从字符串创建复数: complex('1+2j') = {complex_from_str}")

# 复数运算
# 基本算术运算
c1 = 3 + 4j
c2 = 1 + 2j

print(f"加法: {c1} + {c2} = {c1 + c2}")
print(f"减法: {c1} - {c2} = {c1 - c2}")
print(f"乘法: {c1} * {c2} = {c1 * c2}")
print(f"除法: {c1} / {c2} = {c1 / c2}")
print(f"幂运算: {c1} ** 2 = {c1 ** 2}")

# 计算复数的模（绝对值）
# 复数的模是从原点到复数在复平面上表示点的距离
modulus = abs(c1)
print(f"复数的模 (绝对值): abs({c1}) = {modulus}")

# 计算复数的辐角（角度）
import math
angle_radians = math.atan2(c1.imag, c1.real)  # 弧度制
angle_degrees = math.degrees(angle_radians)  # 转换为角度制
print(f"复数的辐角 (弧度): {angle_radians}")
print(f"复数的辐角 (角度): {angle_degrees:.2f}度")

# 使用cmath模块处理复数
import cmath

# 计算复数的平方根
sqrt_result = cmath.sqrt(-1)  # 等同于 1j
print(f"-1的平方根: {sqrt_result}")

# 计算复数的对数、指数、三角函数等
log_result = cmath.log(c1)
exp_result = cmath.exp(c1)
sin_result = cmath.sin(c1)
cos_result = cmath.cos(c1)

print(f"复数的自然对数: {log_result}")
print(f"复数的指数: {exp_result}")
print(f"复数的正弦: {sin_result}")
print(f"复数的余弦: {cos_result}")

# 检查复数是否为实数或虚数
is_real = cmath.isreal(complex(2, 0))  # 虚部为0的复数可以视为实数
is_imag = cmath.isinf(complex(0, 1))  # 实部为0的复数是纯虚数

print(f"是否为实数: isreal(2+0j) = {is_real}")
print(f"是否为纯虚数: isinf(0+1j) = {is_imag}")

# 复数的应用场景
# 1. 科学计算和工程领域
# 2. 信号处理
# 3. 量子力学
# 4. 控制系统
# 5. 流体力学等

# 示例：使用复数表示交流电
# 在电气工程中，复数可以用来表示电压和电流的相位关系
voltage = complex(220, 0)  # 220V 电压，相位角0度
impedance = complex(10, 5)  # 阻抗，电阻10欧姆，电抗5欧姆
current = voltage / impedance  # 根据欧姆定律，电流=电压/阻抗

print(f"电压: {voltage} V")
print(f"阻抗: {impedance} Ω")
print(f"电流: {current} A")
print(f"电流的大小: {abs(current):.2f} A")
print(f"电流的相位角: {math.degrees(math.atan2(current.imag, current.real)):.2f}度")

# 4. 布尔值 (bool)
# 表示真或假，只有两个值：True 和 False
# 在Python中，True 实际上是整数 1 的别名，False 是整数 0 的别名
boolean_true = True
boolean_false = False

print(f"布尔类型: {type(boolean_true)}")
print(f"True 的值: {boolean_true}, False 的值: {boolean_false}")
print(f"True 等于 1: {True == 1}")
print(f"False 等于 0: {False == 0}")

# 布尔运算（逻辑运算）
print(f"逻辑与 (and): True and False = {True and False}")
print(f"逻辑或 (or): True or False = {True or False}")
print(f"逻辑非 (not): not True = {not True}")

# 短路逻辑
# 在 and 运算中，如果第一个操作数为 False，则不会计算第二个操作数
print(f"短路逻辑示例 1: False and print('不会执行') = {False and print('不会执行')}")

# 在 or 运算中，如果第一个操作数为 True，则不会计算第二个操作数
print(f"短路逻辑示例 2: True or print('不会执行') = {True or print('不会执行')}")

# 比较运算返回布尔值
a = 10
b = 20

print(f"{a} == {b}: {a == b}")
print(f"{a} != {b}: {a != b}")
print(f"{a} < {b}: {a < b}")
print(f"{a} > {b}: {a > b}")
print(f"{a} <= {b}: {a <= b}")
print(f"{a} >= {b}: {a >= b}")

# 身份运算符（检查对象的身份，即是否为同一个对象）
x = [1, 2, 3]
y = x  # y 引用同一个列表对象
z = [1, 2, 3]  # z 引用一个新的列表对象（内容相同但不是同一个对象）

print(f"x is y: {x is y}")  # True，因为它们引用同一个对象
print(f"x is z: {x is z}")  # False，因为它们引用不同的对象
print(f"x == z: {x == z}")  # True，因为它们的内容相同

# 成员运算符（检查元素是否在序列或集合中）
numbers = [1, 2, 3, 4, 5]
print(f"3 in numbers: {3 in numbers}")
print(f"6 not in numbers: {6 not in numbers}")

# 布尔转换
# 任何Python对象都可以转换为布尔值
# 使用 bool() 函数或在布尔上下文中（如if语句）

# 以下值在布尔上下文中被视为False：
# - None
# - False
# - 所有数值类型的零：0, 0.0, 0j
# - 空序列和空集合：'', [], (), {}, set(), range(0)

print(f"bool(None): {bool(None)}")
print(f"bool(0): {bool(0)}")
print(f"bool(0.0): {bool(0.0)}")
print(f"bool(''): {bool('')}")
print(f"bool([]): {bool([])}")
print(f"bool({{}}): {bool({})}")

# 所有其他值在布尔上下文中都被视为True
print(f"bool(1): {bool(1)}")
print(f"bool('False'): {bool('False')}")  # 非空字符串为True，即使内容是'False'
print(f"bool([0]): {bool([0])}")  # 非空列表为True，即使包含0

# 布尔值的应用场景
# 1. 条件判断（if语句）
if boolean_true:
    print("条件为真，执行此代码块")

# 2. 循环控制（while语句）
count = 0
while count < 3:
    print(f"循环计数: {count}")
    count += 1

# 3. 表达式过滤
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [num for num in numbers if num % 2 == 0]
print(f"偶数列表: {even_numbers}")

# 4. 布尔值作为计数器
# 由于True等于1，False等于0，它们可以用于计数
results = [True, False, True, True, False]
true_count = sum(results)
print(f"True的数量: {true_count}")

# 5. 三目运算符中的布尔值
value = 10
result = "正数" if value > 0 else "非正数"
print(f"{value}是{result}")

# 5. 字符串 (str)
# 表示文本数据，由Unicode字符序列组成
# Python中的字符串是不可变的，一旦创建就不能修改
string_single_quote = 'Hello, World!'
string_double_quote = "Hello, World!"
string_triple_quote = '''这是一个
多行字符串
可以包含单引号 ' 和双引号 "'''  # 三引号可以定义多行字符串
formatted_string = f"Hello, {integer_example}!"  # f-string，Python 3.6+ 支持
print(f"字符串类型: {type(string_single_quote)}, 示例: {string_single_quote}")
print(f"多行字符串: {string_triple_quote}")
print(f"格式化字符串: {formatted_string}")

# 字符串索引和切片
text = "Python Programming"

# 通过索引访问单个字符
print(f"第一个字符: {text[0]}")
print(f"最后一个字符: {text[-1]}")

# 切片操作
print(f"前6个字符: {text[:6]}")
print(f"从第7个字符开始: {text[6:]}")
print(f"从第7到第18个字符: {text[6:18]}")
print(f"反转字符串: {text[::-1]}")

# 字符串的基本操作
# 连接字符串
greeting = "Hello, " + "Python!"
print(f"字符串连接: {greeting}")

# 重复字符串
stars = "*" * 10
print(f"字符串重复: {stars}")

# 字符串长度
print(f"字符串长度: {len(text)}")

# 检查子字符串
contains_python = "Python" in text
print(f"字符串中包含'Python': {contains_python}")

# 字符串方法
message = "   Hello, Python World!   "

# 大小写转换
print(f"转换为大写: {message.upper()}")
print(f"转换为小写: {message.lower()}")
print(f"首字母大写: {message.title()}")
print(f"第一个单词首字母大写: {message.capitalize()}")
print(f"大小写互换: {message.swapcase()}")

# 去除空白
print(f"去除两端空白: '{message.strip()}'")
print(f"去除左端空白: '{message.lstrip()}'")
print(f"去除右端空白: '{message.rstrip()}'")

# 查找和替换
position = message.find("Python")
print(f"'Python'的位置: {position}")

replaced = message.replace("Python", "Programming")
print(f"替换后的字符串: {replaced}")

# 分割和连接
words = message.split()  # 默认按空白分割
print(f"分割后的列表: {words}")

csv_line = "apple,banana,orange"
fruits = csv_line.split(",")
print(f"按逗号分割: {fruits}")

joined = " ".join(fruits)
print(f"连接后的字符串: {joined}")

# 检查字符串的起始和结束
starts_with_hello = message.startswith("Hello")
ends_with_world = message.endswith("World!")
print(f"以'Hello'开始: {starts_with_hello}")
print(f"以'World!'结束: {ends_with_world}")

# 字符串格式化的不同方式
name = "Alice"
age = 30

# 1. 格式化字符串（f-string，Python 3.6+）
f_str = f"我的名字是 {name}，我今年 {age} 岁。"
print(f"f-string: {f_str}")

# 2. format() 方法
format_str = "我的名字是 {}，我今年 {} 岁。".format(name, age)
print(f"format()方法: {format_str}")

# 3. 旧式的 % 格式化
percent_str = "我的名字是 %s，我今年 %d 岁。" % (name, age)
print(f"%格式化: {percent_str}")

# 格式化数字
pi = 3.1415926
print(f"保留2位小数: {pi:.2f}")
print(f"显示为百分比: {0.75:.1%}")
print(f"科学计数法: {1000000:.2e}")
print(f"格式化宽度: {age:5d}")  # 宽度为5的右对齐

# 原始字符串（不解释转义字符）
original_string = r"C:\Users\name\file.txt"  # 注意前面的r
print(f"原始字符串: {original_string}")

# 字符串的不可变性
# 以下操作会引发TypeError，因为字符串是不可变的
# message[0] = 'h'  # 尝试修改字符串中的字符

# 但可以创建新的字符串
new_message = 'h' + message[1:]
print(f"创建新字符串: {new_message}")

# ========================== 复合数据类型 ==========================

# 6. 列表 (list)
# 有序、可变的元素集合，可以包含不同类型的元素
# 列表是Python中最常用的数据结构之一，提供了丰富的操作方法
list_example = [1, "two", 3.0, True]  # 创建包含不同类型元素的列表
empty_list = []  # 创建空列表
list_from_range = list(range(1, 6))  # 从range对象创建列表
list_from_string = list("hello")  # 从字符串创建列表
print(f"列表类型: {type(list_example)}, 示例: {list_example}")
print(f"从range创建的列表: {list_from_range}")
print(f"从字符串创建的列表: {list_from_string}")

# 列表索引和切片
sample_list = [10, 20, 30, 40, 50]

# 通过索引访问元素（从0开始）
print(f"第一个元素: {sample_list[0]}")
print(f"最后一个元素: {sample_list[-1]}")  # 负索引表示从末尾开始

# 切片操作: list[start:end:step]
print(f"前三个元素: {sample_list[:3]}")  # 从开始到索引3（不包含）
print(f"从索引2到末尾: {sample_list[2:]}")
print(f"索引1到索引3的元素: {sample_list[1:4]}")  # 从索引1到索引4（不包含）
print(f"每隔一个元素: {sample_list[::2]}")  # 步长为2
print(f"列表反转: {sample_list[::-1]}")  # 步长为-1表示反转

# 列表的修改操作
numbers = [3, 1, 4, 1, 5, 9]

# 添加元素
numbers.append(2)  # 在列表末尾添加元素
print(f"添加单个元素后: {numbers}")

numbers.extend([6, 5])  # 添加多个元素
print(f"添加多个元素后: {numbers}")

numbers.insert(2, 100)  # 在指定位置插入元素
print(f"在索引2处插入100后: {numbers}")

# 删除元素
removed = numbers.pop(2)  # 删除并返回指定位置的元素
print(f"删除索引2的元素后: {numbers}, 被删除的元素: {removed}")

numbers.remove(9)  # 删除第一个匹配的值（值不存在会引发ValueError）
print(f"删除值9后: {numbers}")

# 查找元素
index = numbers.index(5)  # 返回第一个匹配值的索引（值不存在会引发ValueError）
print(f"值5的索引位置: {index}")

# 统计元素出现次数
count = numbers.count(1)  # 统计指定值出现的次数
print(f"值1出现的次数: {count}")

# 排序和反转
numbers.sort()  # 原地排序
print(f"排序后: {numbers}")

numbers.reverse()  # 原地反转
print(f"反转后: {numbers}")

# 列表推导式
# 列表推导式是创建列表的简洁方法
squares = [x**2 for x in range(1, 6)]
print(f"列表推导式示例 (1-5的平方): {squares}")

# 带条件的列表推导式
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"1-10中偶数的平方: {even_squares}")

# 嵌套列表推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"二维列表展平: {flattened}")

# 列表的其他常用操作
print(f"列表长度: {len(numbers)}")
print(f"列表最大值: {max(numbers)}")
print(f"列表最小值: {min(numbers)}")
print(f"列表元素之和: {sum(numbers)}")

# 列表复制
# 浅拷贝
list_copy = numbers.copy()
# 或使用切片
list_slice_copy = numbers[:]
print(f"原列表: {numbers}")
print(f"复制的列表: {list_copy}")
print(f"通过切片复制的列表: {list_slice_copy}")

# 7. 元组 (tuple)
# 有序、不可变的元素集合，可以包含不同类型的元素
# 元组与列表类似，但一旦创建就不能修改
# 不可变性使得元组在某些场景下比列表更安全、更高效
tuple_example = (1, "two", 3.0, True)  # 创建元组
empty_tuple = ()  # 创建空元组
single_element_tuple = (42,)  # 注意单个元素的元组需要加逗号，否则会被视为括号表达式
tuple_from_list = tuple([1, 2, 3])  # 从列表创建元组
tuple_from_string = tuple("hello")  # 从字符串创建元组
print(f"元组类型: {type(tuple_example)}, 示例: {tuple_example}")
print(f"空元组: {empty_tuple}")
print(f"单元素元组: {single_element_tuple}")
print(f"从列表创建的元组: {tuple_from_list}")
print(f"从字符串创建的元组: {tuple_from_string}")

# 元组的索引和切片（与列表相同）
t = (10, 20, 30, 40, 50)

# 通过索引访问元素
print(f"第一个元素: {t[0]}")
print(f"最后一个元素: {t[-1]}")

# 切片操作
sliced = t[1:4]  # 获取索引1到3的元素
print(f"切片示例 (t[1:4]): {sliced}")

# 元组的不可变性
# 以下操作会引发TypeError，因为元组是不可变的
# t[0] = 100  # 尝试修改元组元素

# 虽然元组本身不可变，但如果元组中包含可变对象（如列表），这些对象可以被修改
mixed_tuple = (1, 2, [3, 4])
mixed_tuple[2][0] = 30  # 修改元组中的列表元素
print(f"修改元组中的可变对象后: {mixed_tuple}")

# 元组的基本操作
print(f"元组长度: {len(t)}")
print(f"元组最大值: {max(t)}")
print(f"元组最小值: {min(t)}")
print(f"元组元素之和: {sum(t)}")

# 元组的连接和重复
t1 = (1, 2, 3)
t2 = (4, 5, 6)
concatenated = t1 + t2  # 元组连接
print(f"元组连接 (t1 + t2): {concatenated}")

repeated = t1 * 3  # 元组重复
print(f"元组重复 (t1 * 3): {repeated}")

# 元组的解构赋值
# 可以将元组中的元素分别赋值给多个变量
a, b, c = (10, 20, 30)
print(f"元组解构赋值: a={a}, b={b}, c={c}")

# 使用*运算符捕获多个元素
first, *middle, last = (1, 2, 3, 4, 5)
print(f"使用*捕获多个元素: first={first}, middle={middle}, last={last}")

# 元组的常用方法
# 元组的方法较少，因为它是不可变的
count = t.count(20)  # 统计指定值出现的次数
print(f"值20在元组中出现的次数: {count}")

index = t.index(30)  # 返回指定值第一次出现的索引
print(f"值30在元组中的索引位置: {index}")

# 元组的应用场景
# 1. 作为字典的键（因为它是不可变的）
person_dict = {("John", "Doe"): 30, ("Jane", "Smith"): 25}
print(f"使用元组作为字典键: {person_dict}")

# 2. 作为函数的多个返回值
def get_person_info():
    name = "Alice"
    age = 30
    city = "New York"
    return name, age, city  # 实际上返回的是一个元组

person_info = get_person_info()
print(f"函数返回的元组: {person_info}")

# 3. 在不需要修改的数据集合上使用，比列表更高效
# 例如固定的配置项
database_config = ("localhost", 5432, "mydb")
print(f"使用元组存储配置: {database_config}")

# 8. 集合 (set)
# 无序、不重复的元素集合，元素必须是不可变类型
set_example = {1, 2, 3, 4, 5}  # 直接使用花括号创建集合
another_set = set([1, 2, 2, 3, 3, 3])  # 从列表创建集合，自动去重
empty_set = set()  # 创建空集合（注意不能用{}，那会创建空字典）
print(f"集合类型: {type(set_example)}, 示例: {set_example}, {another_set}")

# 集合操作示例
s1 = {1, 2, 3, 4, 5}
s2 = {4, 5, 6, 7, 8}

# 交集：两个集合中共同存在的元素
intersection = s1 & s2  # 或使用 s1.intersection(s2)
print(f"集合交集 (& 或 intersection()): {s1} & {s2} = {intersection}")

# 并集：两个集合中所有不重复的元素
union = s1 | s2  # 或使用 s1.union(s2)
print(f"集合并集 (| 或 union()): {s1} | {s2} = {union}")

# 差集：属于第一个集合但不属于第二个集合的元素
difference = s1 - s2  # 或使用 s1.difference(s2)
print(f"集合差集 (- 或 difference()): {s1} - {s2} = {difference}")

# 对称差集：属于任一集合但不同时属于两个集合的元素
symmetric_diff = s1 ^ s2  # 或使用 s1.symmetric_difference(s2)
print(f"集合对称差集 (^ 或 symmetric_difference()): {s1} ^ {s2} = {symmetric_diff}")

# 集合的包含关系
subset_check = {1, 2}.issubset(s1)  # 检查是否为子集
print(f"{{1, 2}} 是 {s1} 的子集: {subset_check}")

superset_check = s1.issuperset({1, 2})  # 检查是否为超集
print(f"{s1} 是 {{1, 2}} 的超集: {superset_check}")

# 集合的修改操作
s3 = {1, 2, 3}
s3.add(4)  # 添加单个元素
print(f"添加元素 4 后: {s3}")

s3.update([5, 6])  # 添加多个元素
print(f"添加元素 [5, 6] 后: {s3}")

s3.remove(3)  # 删除指定元素（元素不存在会引发KeyError）
print(f"删除元素 3 后: {s3}")

s3.discard(10)  # 删除指定元素（元素不存在不会引发错误）
print(f"尝试删除不存在的元素 10 后: {s3}")

s3.pop()  # 随机删除并返回一个元素
print(f"随机删除一个元素后: {s3}")

s3.clear()  # 清空集合
print(f"清空集合后: {s3}")

# 9. 字典 (dict)
# Python 3.7+ 中，字典是有序的键值对集合，键必须是不可变的
# 字典使用键值对 (key-value) 存储数据，通过键快速查找值
dict_example = {"name": "Alice", "age": 30, "city": "New York"}  # 直接使用花括号创建字典
empty_dict = {}  # 创建空字典
another_dict = dict(name="Bob", age=25)  # 使用dict()函数创建字典
keys_list = ["a", "b", "c"]
values_list = [1, 2, 3]
dict_from_lists = dict(zip(keys_list, values_list))  # 从键列表和值列表创建字典
print(f"字典类型: {type(dict_example)}, 示例: {dict_example}")
print(f"从函数创建字典: {another_dict}")
print(f"从列表创建字典: {dict_from_lists}")

# 字典操作示例
person = {"name": "Alice", "age": 30, "city": "New York"}

# 访问字典值
print(f"访问字典值: name = {person['name']}")
# 使用get()方法安全地访问值（键不存在时返回默认值）
email = person.get("email", "not provided")
print(f"使用get()方法访问不存在的键: email = {email}")

# 添加或修改键值对
person["email"] = "alice@example.com"  # 添加新键值对
person["age"] = 31  # 修改已有键的值
print(f"添加和修改后: {person}")

# 删除键值对
removed_age = person.pop("age")  # 移除指定键并返回其值
print(f"移除'age'键后: {person}, 被移除的值: {removed_age}")

# 随机删除并返回一个键值对（Python 3.7+中默认删除最后一个添加的）
last_item = person.popitem()
print(f"使用popitem()删除后: {person}, 被删除的项: {last_item}")

# 清空字典
person.clear()
print(f"清空后: {person}")

# 字典的遍历
person = {"name": "Bob", "age": 25, "city": "Boston"}

# 遍历键
print("遍历键:")
for key in person.keys():
    print(f"  {key}")

# 遍历值
print("遍历值:")
for value in person.values():
    print(f"  {value}")

# 遍历键值对
print("遍历键值对:")
for key, value in person.items():
    print(f"  {key}: {value}")

# 字典的其他常用方法
# 合并字典（Python 3.9+）
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged_dict = dict1 | dict2  # 使用|操作符合并，相同键会被dict2的值覆盖
print(f"使用|操作符合并字典: {merged_dict}")

# 原地合并字典
dict1.update(dict2)
print(f"使用update()方法合并后: {dict1}")

# 字典推导式
squared_numbers = {x: x**2 for x in range(1, 6)}
print(f"字典推导式示例: {squared_numbers}")

# ========================== 特殊数据类型 ==========================

# 10. NoneType
# 表示空值或无值，只有一个值 None
# None 不等于空字符串、空列表或零，它是一个特殊的单例对象
none_value = None
print(f"None类型: {type(none_value)}, 示例: {none_value}")
print(f"None == '' : {None == ''}")  # False
print(f"None == 0 : {None == 0}")    # False
print(f"None == [] : {None == []}")  # False
print(f"None is None : {None is None}")  # True，因为 None 是单例对象

# None 在布尔上下文中被视为 False
print(f"bool(None) : {bool(None)}")  # False

# None 的常见用途

# 1. 作为函数的默认返回值
# 如果函数没有明确的 return 语句，它会返回 None
def no_return():
    pass

result = no_return()
print(f"没有 return 语句的函数返回: {result}")

# 2. 作为函数参数的默认值
# 当调用函数时如果没有提供参数，就会使用 None
def greet(name=None):
    if name is None:
        return "Hello, stranger!"
    else:
        return f"Hello, {name}!"

print(f"greet() : {greet()}")
print(f"greet('Alice') : {greet('Alice')}")

# 3. 作为尚未赋值的变量的占位符
# 可以先用 None 初始化变量，之后再赋值
user_data = None
# ... 一些代码逻辑 ...
user_data = {"name": "Bob", "age": 30}
print(f"初始化后赋值的变量: {user_data}")

# 4. 表示可选属性或缺失值
# 在字典或对象中，表示某个键或属性不存在
product = {"name": "Phone", "price": 599.99}
stock = product.get("stock", None)
print(f"库存信息: {stock}")

# 5. 作为函数的占位符
# 可以定义一个函数但暂时不实现它，用 None 表示
# 这在大型项目的开发过程中很有用
def future_feature():
    return None

# 6. None 与 is 运算符
# 检查一个变量是否为 None 时，应该使用 is 运算符而不是 ==
# 因为 is 检查的是对象的身份，而 == 检查的是值的相等性
# 对于 None 这种单例对象，使用 is 更高效且更明确
value = None

if value is None:
    print("值是 None")
else:
    print("值不是 None")

# 7. None 不能被索引或调用
# 尝试对 None 进行这些操作会引发 TypeError
try:
    none_value[0]  # 尝试索引 None
except TypeError as e:
    print(f"尝试索引 None 引发错误: {e}")

try:
    none_value()  # 尝试调用 None
except TypeError as e:
    print(f"尝试调用 None 引发错误: {e}")

# 8. None 的字符串表示
# str(None) 返回字符串 'None'
print(f"str(None) : {str(None)}")

# 11. 字节 (bytes)
# 表示字节序列，不可变类型
# bytes 是不可变的字节序列，每个元素是 0-255 范围内的整数

# 创建 bytes 对象的方式

# 1. 使用前缀 b 直接创建
byte_data1 = b'hello'
print(f"1. 直接创建: {byte_data1}")
print(f"   类型: {type(byte_data1)}")
print(f"   长度: {len(byte_data1)}")

# 2. 使用 bytes() 函数从字符串创建（需要指定编码）
byte_data2 = bytes("hello world", "utf-8")
print(f"\n2. 从字符串创建: {byte_data2}")

# 3. 使用 bytes() 函数从可迭代对象创建
# 元素必须是 0-255 范围内的整数
byte_data3 = bytes([104, 101, 108, 108, 111])
print(f"\n3. 从整数列表创建: {byte_data3}")

# 4. 创建指定长度的零字节序列
byte_data4 = bytes(5)
print(f"\n4. 创建零字节序列: {byte_data4}")

# 访问字节元素
# 每个字节可以通过索引访问，返回 0-255 的整数
print(f"\n访问字节元素:")
print(f"byte_data1[0] = {byte_data1[0]}  (字符 'h' 的 ASCII 值)")
print(f"byte_data1[1] = {byte_data1[1]}  (字符 'e' 的 ASCII 值)")

# 切片操作
print(f"\n切片操作:")
print(f"byte_data1[1:4] = {byte_data1[1:4]}")

# 字节字符串的基本操作
print(f"\n字节字符串的基本操作:")
# 连接操作
combined = byte_data1 + b' world'
print(f"连接: {combined}")

# 重复操作
repeated = byte_data1 * 2
print(f"重复: {repeated}")

# 成员检查
print(f"'h' 在 byte_data1 中: {'h' in byte_data1}")
print(f"104 在 byte_data1 中: {104 in byte_data1}")  # 104 是 'h' 的 ASCII 值

# 字节与字符串之间的转换
print(f"\n字节与字符串之间的转换:")
# bytes 转 str
str_data = byte_data1.decode('utf-8')
print(f"bytes 转 str: {str_data}, 类型: {type(str_data)}")

# str 转 bytes
bytes_data = str_data.encode('utf-8')
print(f"str 转 bytes: {bytes_data}, 类型: {type(bytes_data)}")

# 常见的 bytes 方法
print(f"\nbytes 的常见方法:")

# count() - 计算子字节串出现的次数
print(f"'l' 出现的次数: {byte_data1.count(b'l')}")

# find() - 查找子字节串首次出现的位置
print(f"'ll' 首次出现的位置: {byte_data1.find(b'll')}")

# index() - 查找子字节串首次出现的位置（不存在时抛出异常）
print(f"'lo' 首次出现的位置: {byte_data1.index(b'lo')}")

# startswith() - 检查是否以指定字节串开头
print(f"以 'he' 开头: {byte_data1.startswith(b'he')}")

# endswith() - 检查是否以指定字节串结尾
print(f"以 'lo' 结尾: {byte_data1.endswith(b'lo')}")

# split() - 分割字节串
byte_data5 = b'hello,world,bytes'
split_result = byte_data5.split(b',')
print(f"分割结果: {split_result}")

# join() - 连接字节串列表
joined = b'-'.join([b'hello', b'world', b'bytes'])
print(f"连接结果: {joined}")

# hex() - 转换为十六进制表示
hex_repr = byte_data1.hex()
print(f"十六进制表示: {hex_repr}")

# 从十六进制表示创建 bytes
b_from_hex = bytes.fromhex(hex_repr)
print(f"从十六进制转回: {b_from_hex}")

# bytes 的不可变性
print(f"\nbytes 的不可变性:")
try:
    byte_data1[0] = 72  # 尝试修改字节值
except TypeError as e:
    print(f"尝试修改 bytes 引发错误: {e}")

# bytes 的应用场景
print(f"\nbytes 的应用场景:")
print("1. 文件 I/O 操作，特别是二进制文件的读写")
print("2. 网络通信，处理二进制数据")
print("3. 加密算法实现")
print("4. 处理图像、音频等二进制数据")
print("5. 哈希算法计算")

# 示例：使用 bytes 处理二进制数据
# 假设有一个二进制文件的一小部分内容
binary_data = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64])
print(f"\n二进制数据示例 (十六进制): {binary_data.hex()}")
print(f"二进制数据转换为文本: {binary_data.decode('utf-8')}")

# 12. 字节数组 (bytearray)
# 表示可变的字节序列，与 bytes 类似但允许修改
# bytearray 的每个元素也是 0-255 范围内的整数，但可以被修改

# 创建 bytearray 对象的方式

# 1. 使用 bytearray() 函数从 bytes 创建
bytearray1 = bytearray(b'hello')
print(f"1. 从 bytes 创建: {bytearray1}")
print(f"   类型: {type(bytearray1)}")
print(f"   长度: {len(bytearray1)}")

# 2. 使用 bytearray() 函数从字符串创建（需要指定编码）
bytearray2 = bytearray("hello world", "utf-8")
print(f"\n2. 从字符串创建: {bytearray2}")

# 3. 使用 bytearray() 函数从可迭代对象创建
# 元素必须是 0-255 范围内的整数
bytearray3 = bytearray([104, 101, 108, 108, 111])
print(f"\n3. 从整数列表创建: {bytearray3}")

# 4. 创建指定长度的零字节数组
bytearray4 = bytearray(5)
print(f"\n4. 创建零字节数组: {bytearray4}")

# 访问字节数组元素
print(f"\n访问字节数组元素:")
print(f"bytearray1[0] = {bytearray1[0]}  (字符 'h' 的 ASCII 值)")
print(f"bytearray1[1] = {bytearray1[1]}  (字符 'e' 的 ASCII 值)")

# 切片操作
print(f"\n切片操作:")
print(f"bytearray1[1:4] = {bytearray1[1:4]}")

# bytearray 的可变性
print(f"\nbytearray 的可变性:")
# 可以修改单个元素
bytearray1[0] = 72  # 将 'h' 改为 'H'
print(f"修改第一个字节后: {bytearray1}")

# 可以修改切片
bytearray1[1:3] = bytearray([69, 76])  # 将 'e' 改为 'E'，'l' 改为 'L'
print(f"修改切片后: {bytearray1}")

# 字节数组的基本操作
print(f"\n字节数组的基本操作:")
# 连接操作
combined = bytearray1 + bytearray(b' World')
print(f"连接: {combined}")

# 重复操作
repeated = bytearray1 * 2
print(f"重复: {repeated}")

# 成员检查
print(f"'H' 在 bytearray1 中: {'H' in bytearray1}")
print(f"72 在 bytearray1 中: {72 in bytearray1}")  # 72 是 'H' 的 ASCII 值

# 字节数组与字符串之间的转换
print(f"\n字节数组与字符串之间的转换:")
# bytearray 转 str
str_data = bytearray1.decode('utf-8')
print(f"bytearray 转 str: {str_data}, 类型: {type(str_data)}")

# str 转 bytearray
bytearray_data = bytearray(str_data, 'utf-8')
print(f"str 转 bytearray: {bytearray_data}, 类型: {type(bytearray_data)}")

# 常见的 bytearray 方法（与 bytes 类似的方法）
print(f"\nbytearray 的常见方法:")

# count() - 计算子字节序列出现的次数
print(f"'L' 出现的次数: {bytearray1.count(b'L')}")

# find() - 查找子字节序列首次出现的位置
print(f"'LL' 首次出现的位置: {bytearray1.find(b'LL')}")

# startswith() - 检查是否以指定字节序列开头
print(f"以 'HE' 开头: {bytearray1.startswith(b'HE')}")

# endswith() - 检查是否以指定字节序列结尾
print(f"以 'lo' 结尾: {bytearray1.endswith(b'lo')}")

# split() - 分割字节数组
bytearray5 = bytearray(b'hello,world,bytearray')
split_result = bytearray5.split(b',')
print(f"分割结果: {split_result}")

# hex() - 转换为十六进制表示
hex_repr = bytearray1.hex()
print(f"十六进制表示: {hex_repr}")

# bytearray 特有的可变方法
print(f"\nbytearray 特有的可变方法:")

# append() - 添加单个字节（0-255）
bytearray1.append(33)  # 添加感叹号 '!'
print(f"append(33) 后: {bytearray1}")

# extend() - 添加多个字节
bytearray1.extend(b' Python')
print(f"extend(b' Python') 后: {bytearray1}")

# insert() - 在指定位置插入字节
bytearray1.insert(5, 32)  # 在索引 5 处插入空格
print(f"insert(5, 32) 后: {bytearray1}")

# pop() - 移除并返回指定位置的字节
popped = bytearray1.pop(5)  # 移除空格
print(f"pop(5) 返回: {popped}, 移除后: {bytearray1}")

# remove() - 移除第一个匹配的字节
bytearray1.remove(108)  # 移除第一个 'l'
print(f"remove(108) 后: {bytearray1}")

# clear() - 清空字节数组
bytearray_temp = bytearray(b'hello')
bytearray_temp.clear()
print(f"clear() 后: {bytearray_temp}")

# reverse() - 反转字节数组
bytearray_rev = bytearray(b'hello')
bytearray_rev.reverse()
print(f"reverse() 后: {bytearray_rev}")

# resize() - 调整字节数组大小
bytearray_resize = bytearray(b'hello')
bytearray_resize.resize(10)
print(f"resize(10) 后: {bytearray_resize}")

# bytearray 的应用场景
print(f"\nbytearray 的应用场景:")
print("1. 需要频繁修改的二进制数据处理")
print("2. 图像处理中的像素操作")
print("3. 网络协议实现中的数据包构建")
print("4. 二进制数据的原地修改")
print("5. 高效的内存缓冲区操作")

# 示例：使用 bytearray 修改二进制数据
# 假设我们需要修改一个二进制文件的部分内容
binary_data = bytearray([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64])
print(f"\n原始二进制数据: {binary_data.decode('utf-8')}")

# 修改其中的 'World' 为 'Python'
binary_data[6:] = bytearray("Python", 'utf-8')
print(f"修改后二进制数据: {binary_data.decode('utf-8')}")

# 对比 bytes 和 bytearray
print(f"\nbytes 与 bytearray 的对比:")
print("- bytes 是不可变的，bytearray 是可变的")
print("- 两者的大多数方法相同")
print("- bytearray 有额外的可变操作方法")
print("- bytes 更适合哈希表键或需要不可变性的场景")
print("- bytearray 更适合需要频繁修改字节的场景")

# 13. 范围 (range)
# 表示不可变的整数序列，常用于循环中
# range 是一个序列类型，但它是一个惰性计算的对象，不会立即生成所有值

# 创建 range 对象的方式

# 1. range(stop) - 创建从 0 到 stop-1 的整数序列
range1 = range(5)
print(f"1. range(5): {range1}")
print(f"   转换为列表: {list(range1)}")

# 2. range(start, stop) - 创建从 start 到 stop-1 的整数序列
range2 = range(1, 6)
print(f"\n2. range(1, 6): {range2}")
print(f"   转换为列表: {list(range2)}")

# 3. range(start, stop, step) - 创建从 start 到 stop-1 的整数序列，步长为 step
range3 = range(1, 10, 2)
print(f"\n3. range(1, 10, 2): {range3}")
print(f"   转换为列表: {list(range3)}  # 奇数序列")

# 4. 使用负数步长创建递减序列
range4 = range(10, 0, -1)
print(f"\n4. range(10, 0, -1): {range4}")
print(f"   转换为列表: {list(range4)}  # 递减序列")

# 5. 使用负数开始值
range5 = range(-5, 0)
print(f"\n5. range(-5, 0): {range5}")
print(f"   转换为列表: {list(range5)}")

# range 对象的属性
print(f"\nrange 对象的属性:")
print(f"range3.start: {range3.start}")
print(f"range3.stop: {range3.stop}")
print(f"range3.step: {range3.step}")

# 访问 range 元素
print(f"\n访问 range 元素:")
print(f"range3[0]: {range3[0]}  # 访问第一个元素")
print(f"range3[2]: {range3[2]}  # 访问第三个元素")
print(f"range3[-1]: {range3[-1]}  # 访问最后一个元素")

# 切片操作
print(f"\n切片操作:")
print(f"range3[1:4]: {list(range3[1:4])}")

# range 对象的长度
print(f"\nrange 对象的长度:")
print(f"len(range3): {len(range3)}")

# 成员检查
print(f"\n成员检查:")
print(f"3 in range3: {3 in range3}")
print(f"4 in range3: {4 in range3}")
print(f"10 in range3: {10 in range3}")

# 比较操作
# 两个 range 对象如果表示相同的序列，则它们相等
range6 = range(1, 10, 2)
print(f"\n比较操作:")
print(f"range3 == range6: {range3 == range6}  # True，因为它们表示相同的序列")
print(f"range3 == [1, 3, 5, 7, 9]: {range3 == [1, 3, 5, 7, 9]}  # False，因为类型不同")

# range 对象的不可变性
print(f"\nrange 对象的不可变性:")
try:
    range3[0] = 2  # 尝试修改 range 元素
except TypeError as e:
    print(f"尝试修改 range 引发错误: {e}")

# range 的常见用途
print(f"\nrange 的常见用途:")

# 1. for 循环中的计数器
print("1. for 循环中的计数器:")
for i in range(3):
    print(f"  迭代 {i}")

# 2. 遍历序列的索引
print("\n2. 遍历序列的索引:")
fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(f"  索引 {i}: {fruits[i]}")

# 3. 生成固定长度的序列
print("\n3. 生成固定长度的序列:")
zeros = [0] * 5
print(f"  创建包含5个0的列表: {zeros}")

# 4. 与 zip 一起使用，同时获取索引和值
print("\n4. 与 zip 一起使用:")
for i, fruit in zip(range(len(fruits)), fruits):
    print(f"  索引 {i}: {fruit}")

# 5. 列表推导式中的计数器
print("\n5. 列表推导式中的计数器:")
squares = [i*i for i in range(1, 6)]
print(f"  1-5的平方: {squares}")

# range 对象的内存效率
print(f"\nrange 对象的内存效率:")
# 无论范围多大，range 对象占用的内存空间都是相同的
large_range = range(1, 1000000)
small_range = range(1, 5)
print(f"  大范围对象占用的内存: {large_range.__sizeof__()} 字节")
print(f"  小范围对象占用的内存: {small_range.__sizeof__()} 字节")
print(f"  大范围转换为列表占用的内存: {len(large_range)*28} 字节 (估计值)")

# 使用 range 的技巧
print(f"\n使用 range 的技巧:")

# 1. 生成等差数列
print("1. 生成等差数列:")
# 生成 10 到 20 之间的偶数
even_numbers = list(range(10, 21, 2))
print(f"  10-20之间的偶数: {even_numbers}")

# 2. 反向遍历
print("\n2. 反向遍历:")
# 方法1: 使用负数步长
for i in range(5, 0, -1):
    print(f"  反向迭代1: {i}")

# 方法2: 使用 reversed()
for i in reversed(range(1, 6)):
    print(f"  反向迭代2: {i}")

# 3. 生成指定数量的元素
print("\n3. 生成指定数量的元素:")
# 生成 8 个元素，从 2 开始，步长为 3
elements = list(range(2, 2+8*3, 3))
print(f"  8个元素，从2开始，步长3: {elements}")

# 4. 判断数字是否在特定范围内
print("\n4. 判断数字是否在特定范围内:")
number = 7
if number in range(1, 10):
    print(f"  {number} 在 1-9 范围内")

# 5. 创建长度可变的循环
print("\n5. 创建长度可变的循环:")
loop_count = 4
for i in range(loop_count):
    print(f"  可变长度循环: {i}")

# 14. 函数 (function)
# 表示可调用的代码块，是Python中的一等公民
# 函数可以赋值给变量、作为参数传递、作为返回值，也可以在函数内部定义

# 创建函数的方式

# 1. 使用 def 关键字定义函数
def greet(name):
    """这是一个简单的问候函数
    
    参数:
        name (str): 要问候的人的名字
    
    返回:
        str: 问候消息
    """
    return f"Hello, {name}!"

print(f"1. 函数类型: {type(greet)}")
print(f"   函数名: {greet.__name__}")
print(f"   函数文档字符串: {greet.__doc__}")

# 2. 使用 lambda 表达式创建匿名函数
square = lambda x: x * x
print(f"\n2. Lambda 函数: {square}")
print(f"   计算 5 的平方: {square(5)}")

# 3. 使用函数作为参数传递
def apply_function(func, x):
    """将函数应用于给定的值"""
    return func(x)

print(f"\n3. 函数作为参数传递:")
print(f"   apply_function(square, 6) = {apply_function(square, 6)}")
print(f"   apply_function(lambda x: x + 10, 5) = {apply_function(lambda x: x + 10, 5)}")

# 4. 函数作为返回值
def make_multiplier(n):
    """创建一个乘法函数"""
    def multiplier(x):
        return x * n
    return multiplier

print(f"\n4. 函数作为返回值:")
double = make_multiplier(2)
triple = make_multiplier(3)
print(f"   double(5) = {double(5)}")
print(f"   triple(5) = {triple(5)}")

# 函数的参数类型
print(f"\n函数的参数类型:")

# 1. 位置参数
def add(a, b):
    return a + b

print(f"1. 位置参数:")
print(f"   add(3, 5) = {add(3, 5)}")

# 2. 默认参数
def greet_default(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(f"\n2. 默认参数:")
print(f"   greet_default('Alice') = {greet_default('Alice')}")
print(f"   greet_default('Bob', 'Hi') = {greet_default('Bob', 'Hi')}")

# 3. 关键字参数
def describe_person(name, age, city):
    return f"{name} is {age} years old and lives in {city}."

print(f"\n3. 关键字参数:")
print(f"   describe_person(age=30, name='Charlie', city='New York') = {describe_person(age=30, name='Charlie', city='New York')}")

# 4. 可变位置参数 (*args)
def sum_numbers(*args):
    """计算任意数量数字的和"""
    return sum(args)

print(f"\n4. 可变位置参数 (*args):")
print(f"   sum_numbers(1, 2, 3, 4) = {sum_numbers(1, 2, 3, 4)}")
numbers = [5, 6, 7, 8]
print(f"   sum_numbers(*numbers) = {sum_numbers(*numbers)}")  # 解包列表

# 5. 可变关键字参数 (**kwargs)
def print_info(**kwargs):
    """打印关键字参数信息"""
    for key, value in kwargs.items():
        print(f"   {key}: {value}")

print(f"\n5. 可变关键字参数 (**kwargs):")
print_info(name="David", age=25, city="Boston")
person_info = {"name": "Eve", "age": 28, "city": "Chicago"}
print(f"   使用字典解包:")
print_info(**person_info)  # 解包字典

# 6. 混合使用不同类型的参数
def mixed_params(a, b=10, *args, **kwargs):
    print(f"   a = {a}, b = {b}")
    print(f"   args = {args}")
    print(f"   kwargs = {kwargs}")

print(f"\n6. 混合使用不同类型的参数:")
mixed_params(1, 2, 3, 4, 5, x=6, y=7)

# 函数的返回值
print(f"\n函数的返回值:")

# 1. 返回单个值
def get_full_name(first_name, last_name):
    return f"{first_name} {last_name}"

print(f"1. 返回单个值:")
print(f"   get_full_name('John', 'Doe') = {get_full_name('John', 'Doe')}")

# 2. 返回多个值（实际上是返回一个元组）
def get_coordinates():
    return 10, 20  # 返回一个元组 (10, 20)

print(f"\n2. 返回多个值:")
x, y = get_coordinates()  # 解包元组
print(f"   x = {x}, y = {y}")

# 3. 没有明确返回值的函数（默认返回 None）
def no_return():
    pass

print(f"\n3. 没有明确返回值的函数:")
print(f"   no_return() = {no_return()}")

# 函数的属性
print(f"\n函数的属性:")
print(f"函数名: {greet.__name__}")
print(f"函数文档: {greet.__doc__}")
print(f"函数模块: {greet.__module__}")
print(f"函数签名: {greet.__code__.co_argcount} 个参数")

# 函数的作用域
print(f"\n函数的作用域:")

# 全局变量
global_var = "I'm global"

def scope_demo():
    # 局部变量
    local_var = "I'm local"
    print(f"   在函数内部访问局部变量: {local_var}")
    print(f"   在函数内部访问全局变量: {global_var}")
    
    # 修改全局变量需要使用 global 关键字
    global global_var
    global_var = "Modified global"
    
    # 嵌套函数
    def inner_function():
        # 访问外部函数的变量需要使用 nonlocal 关键字
        nonlocal local_var
        local_var = "Modified local"
        print(f"   在内部函数中修改后的局部变量: {local_var}")
    
    inner_function()
    print(f"   内部函数执行后外部函数中的局部变量: {local_var}")

print(f"调用 scope_demo():")
scope_demo()
print(f"函数执行后全局变量: {global_var}")

# 函数装饰器
def decorator(func):
    """一个简单的函数装饰器"""
    def wrapper(*args, **kwargs):
        print(f"   调用函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"   函数 {func.__name__} 调用完成")
        return result
    return wrapper

@decorator

def decorated_function(x):
    return x * 2

print(f"\n函数装饰器:")
result = decorated_function(5)
print(f"   装饰器函数的返回结果: {result}")

# 内置函数示例
print(f"\n内置函数示例:")
print(f"1. len([1, 2, 3]) = {len([1, 2, 3])}")
print(f"2. max(4, 7, 2) = {max(4, 7, 2)}")
print(f"3. min([4, 7, 2]) = {min([4, 7, 2])}")
print(f"4. sum([1, 2, 3, 4]) = {sum([1, 2, 3, 4])}")
print(f"5. sorted([3, 1, 4, 2]) = {sorted([3, 1, 4, 2])}")
print(f"6. list('hello') = {list('hello')}")
print(f"7. dict(a=1, b=2) = {dict(a=1, b=2)}")
print(f"8. set([1, 2, 2, 3]) = {set([1, 2, 2, 3])}")
print(f"9. tuple([1, 2, 3]) = {tuple([1, 2, 3])}")
print(f"10. str(123) = {str(123)}")
print(f"11. int('123') = {int('123')}")
print(f"12. float('3.14') = {float('3.14')}")
print(f"13. bool(0) = {bool(0)}")
print(f"14. abs(-10) = {abs(-10)}")
print(f"15. round(3.14159, 2) = {round(3.14159, 2)}")
print(f"16. range(5) = {list(range(5))}")
print(f"17. enumerate(['a', 'b', 'c']) = {list(enumerate(['a', 'b', 'c']))}")
print(f"18. zip([1, 2, 3], ['a', 'b', 'c']) = {list(zip([1, 2, 3], ['a', 'b', 'c']))}")
print(f"19. map(lambda x: x*2, [1, 2, 3]) = {list(map(lambda x: x*2, [1, 2, 3]))}")
print(f"20. filter(lambda x: x > 2, [1, 2, 3, 4]) = {list(filter(lambda x: x > 2, [1, 2, 3, 4]))}")

# 15. 类和对象
# 用于创建自定义数据类型，实现面向对象编程
# Python是一种面向对象的编程语言，支持封装、继承和多态等OOP特性

# 定义类和创建对象
print(f"\n1. 定义类和创建对象:")

# 定义一个简单的类
class Person:
    """人员类，用于表示人的基本信息"""
    
    # 类属性（所有实例共享）
    species = "Homo sapiens"
    count = 0  # 类变量，用于跟踪创建的实例数量
    
    # 初始化方法（构造函数）
    def __init__(self, name, age):
        """初始化Person实例
        
        参数:
            name (str): 人的姓名
            age (int): 人的年龄
        """
        # 实例属性（每个实例独有）
        self.name = name
        self.age = age
        Person.count += 1  # 每次创建实例时增加计数
    
    # 实例方法
    def greet(self):
        """返回问候消息"""
        return f"Hello, my name is {self.name}."
    
    # 另一个实例方法
    def celebrate_birthday(self):
        """庆祝生日，年龄加1"""
        self.age += 1
        return f"Happy Birthday, {self.name}! You are now {self.age} years old."
    
    # 类方法（使用@classmethod装饰器）
    @classmethod
    def get_species(cls):
        """返回人类物种信息"""
        return f"This is a {cls.species}."
    
    # 静态方法（使用@staticmethod装饰器）
    @staticmethod
    def is_adult(age):
        """判断一个人是否成年
        
        参数:
            age (int): 年龄
        
        返回:
            bool: 如果年龄>=18，返回True，否则返回False
        """
        return age >= 18
    
    # 特殊方法（魔术方法）
    def __str__(self):
        """返回对象的字符串表示"""
        return f"Person(name='{self.name}', age={self.age})"
    
    def __repr__(self):
        """返回对象的正式字符串表示"""
        return f"Person('{self.name}', {self.age})"

# 创建对象（实例化类）
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

print(f"   创建第一个实例: {person1}")
print(f"   创建第二个实例: {person2}")
print(f"   调用实例方法: {person1.greet()}")
print(f"   类属性访问: {Person.species}, {person1.species}")
print(f"   已创建的实例数量: {Person.count}")

# 访问和修改实例属性
print(f"\n2. 访问和修改实例属性:")
print(f"   原始年龄: {person1.name} is {person1.age} years old")
person1.age = 31  # 直接修改实例属性
print(f"   修改后年龄: {person1.name} is {person1.age} years old")
print(f"   通过方法修改属性: {person1.celebrate_birthday()}")

# 调用不同类型的方法
print(f"\n3. 调用不同类型的方法:")
# 实例方法（通过实例调用）
print(f"   实例方法: {person1.greet()}")

# 类方法（可以通过类或实例调用）
print(f"   类方法 (通过类): {Person.get_species()}")
print(f"   类方法 (通过实例): {person1.get_species()}")

# 静态方法（可以通过类或实例调用）
print(f"   静态方法 (通过类): {Person.is_adult(20)}")
print(f"   静态方法 (通过实例): {person1.is_adult(16)}")

# 检查对象类型
print(f"\n4. 检查对象类型:")
print(f"   person1 的类型: {type(person1)}")
print(f"   person1 是否为 Person 类型: {isinstance(person1, Person)}")

# 继承
print(f"\n5. 继承:")

# 定义一个子类（继承Person类）
class Employee(Person):
    """员工类，继承自Person类"""
    
    # 子类的初始化方法
    def __init__(self, name, age, employee_id, department):
        # 调用父类的初始化方法
        super().__init__(name, age)
        # 添加子类特有的属性
        self.employee_id = employee_id
        self.department = department
        self.salary = 0  # 默认工资为0
    
    # 子类特有的方法
    def get_employee_info(self):
        """返回员工的详细信息"""
        return f"Employee {self.employee_id}: {self.name}, Department: {self.department}"
    
    # 重写父类的方法
    def greet(self):
        """重写父类的greet方法"""
        return f"Hello, my name is {self.name}, and I work in {self.department}."
    
    # 添加新方法
    def set_salary(self, salary):
        """设置员工工资"""
        self.salary = salary
        return f"Salary set to {self.salary} for {self.name}"

# 创建子类的实例
employee1 = Employee("Charlie", 35, "E12345", "Engineering")

print(f"   创建Employee实例: {employee1}")
print(f"   调用继承的方法: {employee1.celebrate_birthday()}")
print(f"   调用重写的方法: {employee1.greet()}")
print(f"   调用子类特有的方法: {employee1.get_employee_info()}")
print(f"   调用新方法: {employee1.set_salary(50000)}")
print(f"   employee1 是否为 Person 类型: {isinstance(employee1, Person)}")
print(f"   employee1 是否为 Employee 类型: {isinstance(employee1, Employee)}")
print(f"   Person 类型数量: {Person.count}")  # Employee实例也会增加Person的计数

# 多重继承
print(f"\n6. 多重继承:")

# 定义另一个父类
class Manager:
    """经理类"""
    
    def __init__(self, team_size=0):
        self.team_size = team_size
    
    def manage_team(self):
        """管理团队"""
        return f"Managing a team of {self.team_size} employees."

# 定义一个继承自Employee和Manager的子类
class DepartmentHead(Employee, Manager):
    """部门主管类，继承自Employee和Manager"""
    
    def __init__(self, name, age, employee_id, department, team_size):
        # 调用两个父类的初始化方法
        Employee.__init__(self, name, age, employee_id, department)
        Manager.__init__(self, team_size)
    
    def department_report(self):
        """部门报告"""
        return f"Department: {self.department}, Team Size: {self.team_size}"

# 创建多重继承的实例
dept_head = DepartmentHead("Dave", 45, "E54321", "Engineering", 15)

print(f"   创建DepartmentHead实例: {dept_head}")
print(f"   调用Employee的方法: {dept_head.get_employee_info()}")
print(f"   调用Manager的方法: {dept_head.manage_team()}")
print(f"   调用子类特有的方法: {dept_head.department_report()}")

# 属性访问控制
print(f"\n7. 属性访问控制:")

class BankAccount:
    """银行账户类，演示属性访问控制"""
    
    def __init__(self, account_number, balance=0):
        self.account_number = account_number  # 公共属性
        self._balance = balance  # 私有属性（约定，使用单下划线）
        self.__pin = 1234  # 私有属性（使用双下划线，会被名称修饰）
    
    # getter方法
    def get_balance(self):
        """获取账户余额"""
        return self._balance
    
    # setter方法
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self._balance += amount
            return f"Successfully deposited {amount}. New balance: {self._balance}"
        else:
            return "Deposit amount must be positive"
    
    def withdraw(self, amount, pin):
        """取款"""
        if pin != self.__pin:
            return "Invalid PIN"
        if 0 < amount <= self._balance:
            self._balance -= amount
            return f"Successfully withdrew {amount}. New balance: {self._balance}"
        else:
            return "Invalid withdrawal amount"

# 创建银行账户实例
account = BankAccount("123-456-789", 1000)

print(f"   账户号: {account.account_number}")
print(f"   余额 (通过getter): {account.get_balance()}")
print(f"   存款: {account.deposit(500)}")
print(f"   取款 (正确PIN): {account.withdraw(200, 1234)}")
print(f"   取款 (错误PIN): {account.withdraw(100, 4321)}")
# 尝试直接访问私有属性
print(f"   尝试直接访问 _balance: {account._balance}")  # 可以访问，但按照约定不应该这样做
# print(account.__pin)  # 这会引发AttributeError
print(f"   访问修饰后的私有属性: {account._BankAccount__pin}")  # 可以通过名称修饰后的名称访问

# 数据类（Python 3.7+）
print(f"\n8. 数据类 (Python 3.7+):")

# 导入dataclasses模块
from dataclasses import dataclass

@dataclass
class Product:
    """产品数据类"""
    name: str
    price: float
    quantity: int = 0  # 默认值
    
    # 计算属性
    def total_value(self):
        """计算库存总价值"""
        return self.price * self.quantity

# 创建数据类实例
product1 = Product("Laptop", 999.99, 5)
product2 = Product("Phone", 499.99)

print(f"   创建Product实例: {product1}")
print(f"   创建Product实例 (带默认值): {product2}")
print(f"   计算属性: Total value of {product1.name}s: {product1.total_value()}")

# 自定义对象的应用场景
print(f"\n9. 自定义对象的应用场景:")
print("1. 表示现实世界中的实体（如人、商品、订单等）")
print("2. 封装数据和相关操作，提高代码的组织性和可维护性")
print("3. 通过继承实现代码重用和扩展")
print("4. 实现抽象数据类型和接口")
print("5. 创建可定制的行为和数据结构")

# ========================== 数据类型的检查和转换 ==========================
print(f"\n\n========== 数据类型的检查和转换 ==========")

# 1. 数据类型检查
print(f"\n1. 数据类型检查:")

# 使用type()函数检查类型
print(f"   使用type()函数:")
value_int = 42
value_float = 3.14
value_str = "Hello"
value_list = [1, 2, 3]

print(f"      type({value_int}) = {type(value_int)}, type名称 = {type(value_int).__name__}")
print(f"      type({value_float}) = {type(value_float)}, type名称 = {type(value_float).__name__}")
print(f"      type({value_str}) = {type(value_str)}, type名称 = {type(value_str).__name__}")
print(f"      type({value_list}) = {type(value_list)}, type名称 = {type(value_list).__name__}")

# 使用isinstance()函数检查类型
print(f"\n   使用isinstance()函数:")
print(f"      isinstance({value_int}, int) = {isinstance(value_int, int)}")
print(f"      isinstance({value_float}, float) = {isinstance(value_float, float)}")
print(f"      isinstance({value_str}, str) = {isinstance(value_str, str)}")
print(f"      isinstance({value_list}, list) = {isinstance(value_list, list)}")
print(f"      isinstance({value_int}, (int, float)) = {isinstance(value_int, (int, float))}")  # 检查是否为多个类型中的一个

# 检查自定义对象类型
print(f"\n   检查自定义对象类型:")
person = Person("Alice", 30)
print(f"      isinstance({person}, Person) = {isinstance(person, Person)}")
print(f"      isinstance({person}, object) = {isinstance(person, object)}")  # 所有Python对象都是object的实例

# 2. 基本数据类型转换
print(f"\n2. 基本数据类型转换:")

# 整数转换
print(f"   转换为整数:")
print(f"      int(3.14) = {int(3.14)}")  # 浮点数转整数（截断小数部分）
print(f"      int(\"42\") = {int('42')}")  # 字符串转整数
print(f"      int(\"1010\", 2) = {int('1010', 2)}")  # 二进制字符串转整数
print(f'      int("FF", 16) = {int("FF", 16)}')  # 使用单引号包裹f-string
print(f"      int(True) = {int(True)}, int(False) = {int(False)}")  # 布尔值转整数

# 浮点数转换
print(f"\n   转换为浮点数:")
print(f"      float(42) = {float(42)}")  # 整数转浮点数
print(f"      float(\"3.14\") = {float('3.14')}")  # 字符串转浮点数
print(f"      float(\"2.5e3\") = {float('2.5e3')}")  # 科学计数法字符串转浮点数
print(f"      float(True) = {float(True)}, float(False) = {float(False)}")  # 布尔值转浮点数

# 字符串转换
print(f"\n   转换为字符串:")
print(f"      str(42) = {str(42)}")  # 整数转字符串
print(f"      str(3.14) = {str(3.14)}")  # 浮点数转字符串
print(f"      str([1, 2, 3]) = {str([1, 2, 3])}")  # 列表转字符串
print(f"      str((1, 2, 3)) = {str((1, 2, 3))}")  # 元组转字符串
print(f"      str({person}) = {str(person)}")  # 自定义对象转字符串（调用__str__方法）

# 布尔值转换
print(f"\n   转换为布尔值:")
# 以下值在转换为布尔值时为False
print(f"      bool(0) = {bool(0)}")
print(f"      bool(0.0) = {bool(0.0)}")
print(f"      bool([]) = {bool([])}")
print(f"      bool(()) = {bool(())}")
print(f"      bool({{}}) = {bool({})}")
print(f"      bool(None) = {bool(None)}")
# 其他值转换为布尔值时为True
print(f"      bool(1) = {bool(1)}")
print(f"      bool(\"False\") = {bool('False')}")
print(f"      bool([0]) = {bool([0])}")

# 3. 复合数据类型转换
print(f"\n3. 复合数据类型转换:")

# 列表转换
print(f"   转换为列表:")
print(f"      list((1, 2, 3)) = {list((1, 2, 3))}")  # 元组转列表
print(f"      list(\"Hello\") = {list('Hello')}")  # 字符串转列表
print(f"      list({{1, 2, 3}}) = {list({1, 2, 3})}")  # 集合转列表
print(f"      list({{'a': 1, 'b': 2}}.keys()) = {list({'a': 1, 'b': 2}.keys())}")  # 字典键转列表
print(f"      list(range(5)) = {list(range(5))}")  # range对象转列表

# 元组转换
print(f"\n   转换为元组:")
print(f"      tuple([1, 2, 3]) = {tuple([1, 2, 3])}")  # 列表转元组
print(f"      tuple(\"Hello\") = {tuple('Hello')}")  # 字符串转元组
print(f"      tuple({{1, 2, 3}}) = {tuple({1, 2, 3})}")  # 集合转元组

# 集合转换
print(f"\n   转换为集合:")
print(f"      set([1, 2, 2, 3]) = {set([1, 2, 2, 3])}")  # 列表转集合（去重）
print(f"      set(\"Hello\") = {set('Hello')}")  # 字符串转集合
print(f"      set((1, 2, 3)) = {set((1, 2, 3))}")  # 元组转集合

# 字典转换
print(f"\n   字典相关转换:")
# 从键值对列表创建字典
print(f"      dict([('a', 1), ('b', 2)]) = {dict([('a', 1), ('b', 2)])}")
# 从关键字参数创建字典
print(f"      dict(a=1, b=2) = {dict(a=1, b=2)}")
# 从两个等长列表创建字典（使用zip）
keys = ['a', 'b', 'c']
values = [1, 2, 3]
print(f"      dict(zip({keys}, {values})) = {dict(zip(keys, values))}")

# 4. 类型转换中的注意事项
print(f"\n4. 类型转换中的注意事项:")

# 可能失败的转换
print(f"   可能失败的转换:")
try:
    result = int("abc")
except ValueError as e:
    print(f"      字符串转整数失败: {e}")

try:
    result = float("xyz")
except ValueError as e:
    print(f"      字符串转浮点数失败: {e}")

# 浮点数精度问题
print(f"\n   浮点数精度问题:")
float_value = 0.1 + 0.2
print(f"      0.1 + 0.2 = {float_value}")
print(f"      round(0.1 + 0.2, 1) = {round(0.1 + 0.2, 1)}")

# 5. 高级类型转换和检查
print(f"\n5. 高级类型转换和检查:")

# 使用issubclass()检查类继承关系
print(f"   检查类继承关系:")
print(f"      issubclass(Employee, Person) = {issubclass(Employee, Person)}")
print(f"      issubclass(DepartmentHead, Person) = {issubclass(DepartmentHead, Person)}")
print(f"      issubclass(Person, Employee) = {issubclass(Person, Employee)}")

# 使用type()和isinstance()的区别
print(f"\n   type()和isinstance()的区别:")
# isinstance()会考虑继承关系，而type()不会
print(f"      type(person) == Person = {type(person) == Person}")
print(f"      isinstance(person, Person) = {isinstance(person, Person)}")

# 自定义类型转换方法
print(f"\n   自定义类型转换方法:")
# 在自定义类中实现__int__, __float__, __str__等方法可以自定义类型转换行为
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __float__(self):
        """转换为浮点数（摄氏度值）"""
        return self.celsius
    
    def __str__(self):
        """转换为字符串表示"""
        return f"{self.celsius}°C ({self.celsius * 9/5 + 32}°F)"
    
    def to_fahrenheit(self):
        """转换为华氏度"""
        return self.celsius * 9/5 + 32

temp = Temperature(25)
print(f"      自定义类型转换: float(temp) = {float(temp)}")
print(f"      自定义类型表示: str(temp) = {str(temp)}")
print(f"      自定义转换方法: temp.to_fahrenheit() = {temp.to_fahrenheit()}")

# 6. 实际应用场景
print(f"\n6. 实际应用场景:")
print("   1. 输入处理: 将用户输入的字符串转换为所需的数据类型")
print("   2. 数据验证: 检查数据是否为预期的类型")
print("   3. 数据格式化: 在不同数据表示形式之间转换")
print("   4. 多态实现: 根据对象类型执行不同的操作")
print("   5. 序列化和反序列化: 在数据存储和传输时进行类型转换")

# 总结：
# Python的数据类型系统非常灵活，既包含基本数据类型如整数、浮点数、字符串等，
# 也包含复合数据类型如列表、元组、集合和字典，以及一些特殊的数据类型如None、函数和自定义对象等。
# 掌握类型检查和转换是编写健壮Python程序的重要基础。