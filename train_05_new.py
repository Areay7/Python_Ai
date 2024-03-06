import pandas as pd
import chardet
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Set the font to Arial Unicode MS
plt.rcParams['axes.unicode_minus'] = False  # Resolve the issue of the negative sign '-' being displayed as a square
# 检测文件编码格式
with open('data_06_01.csv', 'rb') as f:
    result = chardet.detect(f.read())
# 获取检测到的编码格式
encoding = result['encoding']
# 使用检测到的编码格式读取文件
df = pd.read_csv('data_06_01.csv', encoding=encoding)
df['日期'] = pd.to_datetime(df['日期'])  # 将日期列转换为日期时间类型
df.dropna(inplace=True)  # 删除缺失值
# 绘制折线图
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(df['日期'], df['销量'], marker='o', linestyle='-')
plt.title('餐厅每日营业额')
plt.xlabel('日期')
plt.ylabel('销量')
plt.grid(True)
plt.tight_layout()
# 保存图形为本地文件
plt.savefig('first.jpg')
# 显示图形
plt.show()
