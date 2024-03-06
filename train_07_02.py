# 第2题(代码):
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# 假设data是你的样本数据
data = [
(0, 170, 65, 'Normal'),
    (1, 160, 80, 'Obese'),
(0, 180, 80, 'Normal'),
    (1, 160, 40, 'thin'),
(0, 170, 65, 'Normal'),
    (1, 160, 80, 'Obese'),
(0, 170, 65, 'Normal'),
    (1, 160, 45, 'thin'),
]
# 拆分数据集
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
# 提取特征和标签
X_train = [(x[0], x[1], x[2]) for x in train_data]
y_train = [x[3] for x in train_data]
X_test = [(x[0], x[1], x[2]) for x in test_data]
y_test = [x[3] for x in test_data]
# 创建KNN分类器，选择适当的邻居数量（这里选择3个邻居）
knn = KNeighborsClassifier(n_neighbors=3)
# 训练模型
knn.fit(X_train, y_train)
# 对测试数据进行预测
y_pred = knn.predict(X_test)
# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
# 对未知数据进行分类
unknown_data = [(1, 160, 40)]  # 未知数据，性别为1（女性），身高165，体重70
prediction = knn.predict(unknown_data)
print(f"Prediction for unknown data: {prediction}")
