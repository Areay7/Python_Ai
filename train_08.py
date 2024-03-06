from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
# 获取模拟数据
X = np.array([[1, 1, 1, 1, 1, 1, 1],
              [2, 3, 2, 3, 2, 2, 3],
              [3, 3, 2, 3, 3, 2, 3],
              [1, 2, 2, 1, 2, 1, 2],
              [2, 3, 1, 3, 1, 2, 3],
              [6, 2, 30, 3, 33, 2, 71]])
# 训练
kmeansPredictor = KMeans(n_clusters=3, n_init=10).fit(X)
# 原始数据分
category = kmeansPredictor.predict(X)
print('分类情况:', category)
print('=' * 30)
def predict(element):
    result = kmeansPredictor.predict(element)
    print('预测结果:', result)
    print('相似元素:\n', X[category == result])
# 测试
predict([[1, 2, 3, 3, 1, 3, 1]])
print('=' * 30)
predict([[5, 2, 23, 2, 21, 5, 51]])
# 画一个饼图
def plot_pie_chart(category):
    labels, counts = np.unique(category, return_counts=True)
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Cluster Distribution')
    plt.show()
# Visualize the clustering results with a pie chart
plot_pie_chart(category)
