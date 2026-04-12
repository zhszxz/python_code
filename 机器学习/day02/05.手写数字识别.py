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


if __name__ == '__main__':
    show_digit(9)
