import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Set the font to Arial Unicode MS
plt.rcParams['axes.unicode_minus'] = False  # Resolve the issue of the negative sign '-' being displayed as a square
# 读取Excel文件
file_path = 'student.xlsx'
excel_data = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
# 获取所有工作表的名称
sheet_names = list(excel_data.keys())
# 定义绘制柱状图的函数
def plot_bar_chart(data, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='学号', y='成绩', data=data)
    plt.title(title)
    plt.xlabel('学号')
    plt.ylabel('成绩')
    plt.show()
# 定义绘制热力图的函数
def plot_heatmap(data, title):
    plt.figure(figsize=(12, 8))
    sns.heatmap(data.pivot_table(index='学号', columns='姓名', values='成绩'), cmap='YlGnBu', annot=True, fmt=".1f")
    plt.title(title)
    plt.show()
# 定义绘制折线图和扇形图的函数
def plot_line_and_pie_chart(data, title):
    plt.figure(figsize=(12, 6))
    # 计算每个学号的成绩平均值和标准差
    average_scores = data.groupby('学号')['成绩'].mean()
    std_dev_scores = data.groupby('学号')['成绩'].std()
    # 绘制折线图
    average_scores.plot(label='平均成绩', marker='o')
    # 划分扇形图区间
    bins = [50, 60, 90, 100]
    labels = ['50-60', '60-90', '90-100']
    # 将成绩分布划分到不同区间
    data['成绩区间'] = pd.cut(data['成绩'], bins=bins, labels=labels, right=False)
    # 计算每个区间的学生人数
    pie_data = data.groupby('成绩区间')['学号'].count()
    # 绘制扇形图
    plt.figure(figsize=(8, 8))
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
    plt.title('学号成绩分布扇形图')
    plt.show()
    # 输出每个班级的成绩平均值
    average_class_score = data['成绩'].mean()
    print(f'{title}班级成绩平均值：{average_class_score}\n')
# 分别绘制每个班级的柱状图、热力图、折线图和扇形图（成绩平均值和标准差）
for sheet_name in sheet_names:
    sheet_data = excel_data[sheet_name]
    plot_bar_chart(sheet_data, f'{sheet_name}班级学生成绩柱状图')
    plot_heatmap(sheet_data, f'{sheet_name}班级学生成绩热力图')
    plot_line_and_pie_chart(sheet_data, f'{sheet_name}班级学生成绩折线图和扇形图')

