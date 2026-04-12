"""
案例: KNN算法 手写数字识别案例.

介绍:
    每张图片都是由 28 * 28 像素组成的, 即: csv文件中每一行都有 784个像素点, 表示图片(每个像素)的 颜色.
    最终构成图像.
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib
from collections import Counter


# 1. 接收索引, 展示该索引行数据对应的图片.
def show_digit(idx):
    # 1.读取数据集
    df = pd.read_csv('./data/手写数字识别.csv')

    # 2.校验索引
    if idx < 0 or idx >= len(df):
        print('索引越界')
        return

    # 3.获取特征和标签数据
    features = df.iloc[:, 1:]
    labels = df.iloc[:, 0]

    # 4.查看索引行的标签
    print(f'图片对应的数字是: {labels.iloc[idx]}')
    print(f'所有的标签的分布情况: {Counter(labels)}')

    # 5.查看索引行特征数据形状
    print(f'特征数据形状: {features.iloc[idx].shape}')  # (784,)

    # 6.将索引行特征数据转为 28 * 28
    feature = features.iloc[idx].values.reshape(28, 28)

    # 7.绘制灰度图
    plt.imshow(feature, cmap=plt.cm.gray)
    plt.axis('off')  # 关闭坐标轴
    plt.show()


# 2. 训练模型, 并保存训练好的模型.
def train_model():
    # 1. 加载数据集.
    df = pd.read_csv('./data/手写数字识别.csv')
    # 2. 数据的预处理.
    # 2.1 拆分出特征列.
    x = df.iloc[:, 1:]
    # 2.2 拆分出标签列.
    y = df.iloc[:, 0]
    # 2.3 打印特征和标签的形状
    print(f'x的形状: {x.shape}')
    print(f'y的形状: {y.shape}')
    print(f'查看所有的标签的分布情况: {Counter(y)}')
    # 2.4 对特征归一化
    x = x / 255
    # 2.5 拆分训练集和测试集.
    # 参数一：训练集 参数二：测试集 参数三：随机种子 参数四：分层抽样依据
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=21, stratify=y)
    # 3.训练模型
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train, y_train)
    # 4.模型评估
    print(f'准确率: {estimator.score(x_test, y_test)}')
    print(f'准确率: {accuracy_score(y_test, estimator.predict(x_test))}')
    # 5.保存模型
    joblib.dump(estimator, './model/手写数字识别.pkl')
    print('保存模型成功!')


# 3. 测试模型.
def use_model():
    # 1.加载图片为ndarray
    x = plt.imread('./data/demo.png')
    print(f"ndarray的形状：{x.shape}")
    # 2.绘制图片
    plt.imshow(x, cmap=plt.cm.gray)
    plt.show()
    # 3.将图片转为特征向量
    print(x.reshape(1, 784).shape)
    x = x.reshape(1, -1)  # 效果同上，-1表示有多少转多少
    # 4.使用模型进行预测
    estimator = joblib.load('./model/手写数字识别.pkl')
    print(f'预测结果为: {estimator.predict(x)}')


if __name__ == '__main__':
    # show_digit(9)
    # train_model()
    use_model()
