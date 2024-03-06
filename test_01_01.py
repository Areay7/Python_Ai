#(1)
# data = eval(input('请输入若干自然数的列表：'))
# avg = sum(data) / len(data)
# avg = round(avg, 3)
# print('平均值：', avg)

#(2)
# data = eval(input('请输入若干自然数的列表：'))
# print('降序后的列表：',sorted(data, reverse=True))

#(3)
# # data = eval(input('请输入若干自然数的列表：'))
# data = map(str, data)
# length = list(map(len,data))
# print('每个元素的位数：',length)

#(4)
# data = eval(input('请输入若干自然数的列表：'))
# print('绝对值最大的数字：',max(data, key=abs))

#(5)
# from  operator import mul
# from functools import reduce
#
# data = eval(input('请输入包含若干自然数的列表：'))
# print('乘积：',reduce(mul,data))

#(6)
# from operator import mul
# from functools import reduce
# vec1=eval(input('请输入第一个向量：'))
# vec2=eval(input('请输入第二个向量：'))
# print('内积',sum(map(mul,vec1,vec2)))