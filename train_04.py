import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 设置中文字体为 SimHei 或其他支持中文的字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取 Excel 文件
file_path = '随机生成的学生成绩.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=None)

# 分别读取两个工作表的数据
class1_data = excel_data['班级1']
class2_data = excel_data['班级2']

# 可视化 - 柱状图
plt.figure(figsize=(10, 6))

# 计算每个班级的柱状图位置
class1_x = np.arange(len(class1_data))
class2_x = np.arange(len(class2_data))

# 绘制第一个班级的柱状图
plt.bar(class1_x - 0.2, class1_data['成绩'], width=0.4, label='班级1', color='blue')  # 这里的 '成绩' 是你数据中成绩所在列的列名
# 绘制第二个班级的柱状图
plt.bar(class2_x + 0.2, class2_data['成绩'], width=0.4, label='班级2', color='orange')  # 这里的 '成绩' 是你数据中成绩所在列的列名

plt.xlabel('学生编号')
plt.ylabel('成绩')
plt.title('两个班级学生成绩对比柱状图')
plt.xticks(ticks=np.arange(max(len(class1_data), len(class2_data))),
           labels=np.arange(1, max(len(class1_data), len(class2_data)) + 1))
plt.legend()  # 添加图例
plt.show()

# 合并两个班级的数据
df = pd.concat([class1_data['成绩'], class2_data['成绩']], axis=1)
df.columns = ['班级1', '班级2']

# 绘制热力图
plt.figure(figsize=(8, 6))
sns.heatmap(df.T, cmap='hot', annot=False, fmt=".1f")

# 设置班级标签和其他标签
plt.xlabel('学生编号')
plt.ylabel('班级')
plt.title('两个班级学生成绩热力图')

# 设置y轴标签为班级1和班级2
plt.yticks(ticks=[0.5, 1.5], labels=['班级1', '班级2'])

# 显示图形
plt.tight_layout()
plt.show()

# 计算两个班级的平均值和标准差
mean_class1 = class1_data['成绩'].mean()
mean_class2 = class2_data['成绩'].mean()
std_class1 = class1_data['成绩'].std()
std_class2 = class2_data['成绩'].std()

# 绘制平均值和标准差的柱状图
plt.figure(figsize=(8, 6))

# 设置标签和位置
labels = ['班级1 平均值', '班级2 平均值', '班级1 标准差', '班级2 标准差']
values = [mean_class1, mean_class2, std_class1, std_class2]
positions = np.arange(len(labels))

colors = ['blue', 'orange', 'green', 'red']  # 柱状图颜色

# 绘制柱状图
bars = plt.bar(positions, values, align='center', alpha=0.5, color=colors)
plt.xticks(positions, labels)
plt.ylabel('数值')
plt.title('两个班级学生成绩的平均值和标准差')

# 添加图例
legend_labels = ['班级1 平均值', '班级2 平均值', '班级1 标准差', '班级2 标准差']
plt.legend(bars, legend_labels)

plt.show()

# 可视化 - 折线图
plt.figure(figsize=(10, 6))

# 绘制第一个班级的折线图
plt.plot(class1_data['学生编号'], class1_data['成绩'], marker='o', label='班级1', color='blue')  # 这里的 '成绩' 是你数据中成绩所在列的列名
# 绘制第二个班级的折线图
plt.plot(class2_data['学生编号'], class2_data['成绩'], marker='o', label='班级2', color='orange')  # 这里的 '成绩' 是你数据中成绩所在列的列名

plt.xlabel('学生编号')
plt.ylabel('成绩')
plt.title('两个班级学生成绩对比折线图')
plt.legend()  # 添加图例
plt.grid(True)  # 显示网格线
plt.show()

# 合并两个班级的成绩数据
merged_data = pd.concat([class1_data['成绩'], class2_data['成绩']])

# 统计各个班级在不同分数段的人数
class1_counts = pd.cut(class1_data['成绩'], bins=[60, 70, 80, 90, 100], include_lowest=True).value_counts().sort_index()
class2_counts = pd.cut(class2_data['成绩'], bins=[60, 70, 80, 90, 100], include_lowest=True).value_counts().sort_index()

# 统计合并后数据的各个分数段人数
merged_counts = pd.cut(merged_data, bins=[60, 70, 80, 90, 100], include_lowest=True).value_counts().sort_index()

# 绘制饼状图
labels = ['60-70分', '70-80分', '80-90分', '90-100分']
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

plt.figure(figsize=(10, 6))

plt.subplot(1, 2, 1)
plt.pie(class1_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('班级1成绩分布')

plt.subplot(1, 2, 2)
plt.pie(class2_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('班级2成绩分布')

plt.tight_layout()
plt.show()

# 绘制合并后数据的饼状图
plt.figure(figsize=(6, 6))
plt.pie(merged_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('两个班级成绩合并后的分布')

plt.tight_layout()
plt.show()