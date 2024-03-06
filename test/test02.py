import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
file_path = 'stock.xlsx'  # 请替换为您的文件路径
df = pd.read_excel(file_path)

# 重命名并设置日期为索引
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df.set_index('Date', inplace=True)

# 删除收盘价为0的行
df_filtered = df[(df['A'] != 0) & (df['B'] != 0)]

# 计算日度收益率
df_filtered['Return_A'] = df_filtered['A'].pct_change()
df_filtered['Return_B'] = df_filtered['B'].pct_change()

# 绘制收盘价曲线图
plt.figure(figsize=(10, 6))
plt.plot(df_filtered.index, df_filtered['A'], label='Stock A', color='blue')
plt.plot(df_filtered.index, df_filtered['B'], label='Stock B', color='orange')
plt.title('Closing Prices of Stocks A and B')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
