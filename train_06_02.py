import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 读取修改后的CSV文件（假设列名为"日期"和"销量"）
file_path = 'data_06_02.csv'  # 修改后的文件路径
df = pd.read_csv(file_path, encoding='utf-8')  # 使用GBK编码格式读取
# 将"日期"列转换为日期时间格式（指定日期格式）
df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d', errors='coerce')
# 删除日期中无效的行
df = df.dropna(subset=['日期'])
# 提取2017年的数据
df_2017 = df[df['日期'].dt.year == 2017]
# 根据季度对营业额进行求和
df_2017['季度'] = df_2017['日期'].dt.quarter
revenue_per_quarter = df_2017.groupby('季度')['销量'].sum()
# 定义饼状图标签
labels = ['第一季度', '第二季度', '第三季度', '第四季度']
# 绘制饼状图
plt.figure(figsize=(8, 6))
plt.pie(revenue_per_quarter, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('2017年各个季度营业额分布情况')
plt.axis('equal')  # 保持长宽相等，使饼状图为圆形
# 调整图形大小（按比例缩小20%）
plt.gcf().set_size_inches(8 * 0.8, 6 * 0.8)
# 调整标签的位置和字体大小
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
plt.rcParams.update({'font.size': 12})
# 保存图形为本地文件
plt.savefig('third.jpg')
# 显示饼状图
plt.show()
