import pandas as pd
import chardet
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
# 检测文件编码格式
with open('data_06_01.csv', 'rb') as f:
    result = chardet.detect(f.read())
# 获取检测到的编码格式
encoding = result['encoding']
# 使用检测到的编码格式读取文件
df = pd.read_csv('data_06_01.csv', encoding=encoding)
df.dropna(inplace=True)  # 删除缺失值
# 将 '日期' 列转换为日期时间类型
df['日期'] = pd.to_datetime(df['日期'])
# 添加 'Month' 列，用于存储月份信息
df['Month'] = df['日期'].dt.month
# 按月份分组并计算每个月份的总销量
monthly_sales = df.groupby('Month')['销量'].sum()
# 绘制柱状图
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='bar', color='skyblue')
plt.title('餐厅每月销量')
plt.xlabel('月份')
plt.ylabel('销量')
plt.xticks(rotation=0)  # 保持月份标签水平显示
plt.tight_layout()
# 保存图形为本地文件
plt.savefig('second.jpg')
# 显示图形
plt.show()
