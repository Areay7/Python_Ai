import pandas as pd
# 读取CSV文件，假设列名为 '日期' 和 '销量'，文件编码格式为GBK
df = pd.read_csv('data_06_01.csv', encoding='UTF-8')
# 删除缺失值
df.dropna(inplace=True)
# 将 '日期' 列转换为日期时间类型
df['日期'] = pd.to_datetime(df['日期'])
# 添加 'Month' 列，用于存储月份信息
df['Month'] = df['日期'].dt.month
# 按月份分组并计算每个月份的总销量
monthly_sales = df.groupby('Month')['销量'].sum()
# 计算相邻两个月份的销量差值
monthly_sales_diff = monthly_sales.diff()
# 找出涨幅最大的月份
max_increase_month = monthly_sales_diff.idxmax()
# 将涨幅最大的月份写入文件 maxMonth.txt
with open('maxMonth.txt', 'w', encoding='utf-8') as file:
    file.write(f'涨幅最大的月份为：{max_increase_month}月')
print(f'涨幅最大的月份为：{max_increase_month}月')
