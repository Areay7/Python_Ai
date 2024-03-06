# 第1题(代码):
# 提示用户输入包含若干自然数的列表，并使用 eval() 函数将输入字符串转换为列表
data = eval(input('请输入若干自然数的列表：'))

# 计算列表中所有元素的和，并除以列表长度，得到平均值
avg = sum(data) / len(data)

# 使用 round() 函数将平均值保留三位小数
avg = round(avg, 3)

# 打印计算得到的平均值
print('平均值：', avg)

# 第2题(代码):
# 提示用户输入包含若干自然数的列表
def second(nums):
    sorted_data = sorted(nums, key=int, reverse=True)
    return sorted_data
lb = input("请输入自然数列表，用空格分隔: ").split()
if lb:
    result = second(lb)
    print(f"这些自然数的降序为: {result}")
else:
    print("未输入有效的自然数列表")
# 使用 sorted() 函数对列表进行降序排序，reverse=True 表示降序
sorted_data = sorted(data, reverse=True)

# 第3题(代码):
# 提示用户输入包含若干自然数的列表，并使用 eval() 函数将输入字符串转换为列表
data = eval(input('请输入若干自然数的列表：'))

# 使用 map() 函数将列表中的每个元素转换为字符串类型
data = map(str, data)

# 使用 map() 函数和 len() 函数获取每个元素的位数
length = list(map(len, data))

# 打印每个元素的位数
print('每个元素的位数：', length)



# 第4题(代码):
# 提示用户输入包含若干自然数的列表，并使用 eval() 函数将输入字符串转换为列表
data = eval(input('请输入包含若干自然数的列表:'))

# 使用 max() 函数找到列表中绝对值最大的数字，key=abs 表示按绝对值进行比较
max_value = max(data, key=abs)

# 打印绝对值最大的数字
print('绝对值最大的数字：', max_value)
# 第5题(代码):
# 导入 operator 模块中的 mul 函数，用于乘法操作
from operator import mul

# 导入 functools 模块中的 reduce 函数，用于对可迭代对象进行累积操作
from functools import reduce

# 提示用户输入包含若干自然数的列表，并使用 eval() 函数将输入字符串转换为列表
data = eval(input('请输入包含若干自然数的列表：'))

# 使用 reduce() 函数和 mul() 函数对列表中的所有元素进行乘积累积
# reduce(mul, data) 相当于 mul(mul(mul(data[0], data[1]), data[2]), ...)
result = reduce(mul, data)

# 打印列表中所有元素的乘积
print('乘积：', result)
# 第6题(代码):
# 导入 operator 模块中的 mul 函数，用于乘法操作
from operator import mul

# 导入 functools 模块中的 reduce 函数，用于对可迭代对象进行累积操作
from functools import reduce

# 提示用户输入第一个向量，并使用 eval() 函数将输入字符串转换为列表
vec1 = eval(input('请输入第一个向量：'))

# 提示用户输入第二个向量，并使用 eval() 函数将输入字符串转换为列表
vec2 = eval(input('请输入第二个向量：'))

# 使用 map() 函数对两个向量对应位置的元素进行逐个相乘，生成一个乘法结果的迭代器
# 然后使用 sum() 函数对这些乘积结果进行求和，得到内积
inner_product = sum(map(mul, vec1, vec2))

# 打印向量的内积
print('内积：', inner_product)
