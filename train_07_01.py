import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Set the font to Arial Unicode MS
plt.rcParams['axes.unicode_minus'] = False  # Resolve the issue of the negative sign '-' being displayed as a square
# 读取CSV文件
data = pd.read_csv('data.csv', encoding='UTF-8')
# 提取特征和目标变量
X = data[['年龄']]
y = data['孩子身高']
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
# 训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)
# 假设预测一个特定年龄的孩子身高
specified_age = 14
specified_age_data = [[specified_age]]
predicted_height = model.predict(specified_age_data)
print(f"预测的身高为: {predicted_height[0]}")
# 绘制年龄与孩子身高的线性回归图
plt.scatter(X, y, color='blue', label='数据点')  # 修改散点颜色为蓝色
plt.plot(X, model.predict(X), color='black', linewidth=2, label='线性回归')  # 修改线的颜色为黑色
plt.scatter(specified_age, predicted_height[0], color='red', label='预测值')  # 添加预测值散点，颜色为红色
# 设置图例中文
font = FontProperties(fname='/System/Library/Fonts/STHeiti Medium.ttc', size=12)
plt.legend(prop=font)  # 设置图例字体属性
plt.xlabel('年龄')
plt.ylabel('孩子身高')
plt.title('年龄与孩子身高的线性回归模型')
plt.show()
