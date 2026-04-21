"""
案例:
    演示逻辑回归模型实现 癌症预测.

逻辑回归模型介绍:
    概述:
        属于有监督学习, 即: 有特征, 有标签, 且标签是离散的.
        主要适用于: 二分类.
    原理:
        把线性回归处理后的预测值 -> 通过 Sigmoid激活函数, 映射到[0, 1] 概率 -> 基于自定义的阈值, 结合概率来 分类.
    损失函数:
        极大似然估计函数的 负数形式.

回顾: 机器学习项目流程
    1. 加载数据.
    2. 数据预处理.
    3. 特征工程(提取, 预处理...)
    4. 模型训练.
    5. 模型预测.
    6. 模型评估.
"""

# 导包
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression  # 逻辑回归模型
from sklearn.preprocessing import StandardScaler  # 标准化
from sklearn.model_selection import train_test_split  # 训练集和测试集分割
from sklearn.metrics import accuracy_score  # 模型评估

# 1.数据加载
data = pd.read_csv("./data/breast-cancer-wisconsin.csv")

# 2.数据预处理
data = data.replace("?", np.nan)  # 参一：待替换的值 参二：替换为的值
data.dropna(axis=0, inplace=True)  # 删除有缺失值的行，inplace：True直接修改原数据
data.info()

# 3.特征工程
# 3.1 提取特征和标签
x = data.iloc[:, 1:-1]
y = data.iloc[:, -1]
# 3.2 查看特征和标签
print(f'特征(x): {x[:5]}')
print(f'标签(y): {y[:5]}')
print(f'特征(x)的形状: {x.shape}')
print(f'标签(y)的形状: {y.shape}')
# 3.3 切割训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=23)
# 3.4 标准化
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 4.模型训练
estimator = LogisticRegression()
estimator.fit(x_train, y_train)

# 5.模型预测
y_predict = estimator.predict(x_test)
print(f'预测结果: {y_predict}')

# 6.模型评估
print(f'预测前评估, 正确率: {estimator.score(x_test, y_test)}')  # 测试集的特征, 标签.
print(f'预测后评估, 正确率: {accuracy_score(y_test, y_predict)}')  # 测试集的标签, 预测值.

# 思考: 逻辑回归模型能用 准确率来评测吗?
# 答案: 可以, 但是结果不精准, 因为逻辑回归模型主要用于 二分类, 即: A类还是B类, 不能说 97%的A类, 3%的B类.
# 所以要通过 混淆矩阵来评测, 即: 精确率, 召回率, F1值, ROC曲线, AUC值.
