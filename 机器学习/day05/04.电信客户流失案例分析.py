"""
案例:
    电信客户流失分析.

目的:
    1. 演示逻辑回归的相关操作, 主要是: 二分法(流失, 不流失)
    2. 演示逻辑回归的评估操作, 主要是: 混淆矩阵, 准确率, 召回率, F1值, ROC曲线, AUC值, 分类评估报告(了解)
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, \
    classification_report
from sklearn.model_selection import train_test_split


# 1. 定义函数, 用于实现: 数据预处理.
def dm01_数据预处理():
    # 1. 读取数据
    data = pd.read_csv('./data/churn.csv')
    data.info()

    # 2. 对字符串数据 Churn gender 做独热编码(one-hot)处理
    # 独热编码：把文本数据的每一个枚举值转成一个名为 原列名_枚举值 的数值列，这些列一行只有一个值为1，其余为0
    data = pd.get_dummies(data, columns=['Churn', 'gender'])
    data.info()
    print(data.head(10))

    # 3. 删除多余列
    data.drop(['gender_Male', 'Churn_No'], axis=1, inplace=True)
    print(data.head(10))

    # 4. 修改列名
    data.rename(columns={'Churn_Yes': 'flag'}, inplace=True)
    print(data.head(10))

    # 5. 查看数据集标签是否均衡
    print(data.flag.value_counts())  # False -> 不流失, True -> 流失


# 2. 定义函数, 用于显示: 月度会员的流失情况.
def dm02_会员流失可视化情况():
    # 1. 读取数据.
    data = pd.read_csv('./data/churn.csv')

    # 2. 对上述的数据做 热编码处理.
    data = pd.get_dummies(data)

    # 3. 删除列
    data.drop(['gender_Male', 'Churn_No'], axis=1, inplace=True)

    # 4. 修改列名.
    data.rename(columns={'Churn_Yes': 'flag'}, inplace=True)

    # 5. 查看数据集的分布情况.
    print(data.flag.value_counts())
    '''
    ['Partner_att', 'Dependents_att', 'landline', 'internet_att',
       'internet_other', 'StreamingTV', 'StreamingMovies', 'Contract_Month',
       'Contract_1YR', 'PaymentBank', 'PaymentCreditcard', 'PaymentElectronic',
       'MonthlyCharges', 'TotalCharges', 'flag', 'gender_Female']
    '''
    print(data.columns)  # 查看所有列名.

    # 6. 通过计数柱状图, 绘制(月度)会员的流失情况.
    # 参数x: x轴的列名(是否是月度会员, 0 -> 不是会员, 1 -> 是会员)
    # 参数hue: 根据hue的值, 将数据进行分类(False -> 不流失, True -> 流失)
    sns.countplot(data, x='Contract_Month', hue='flag')
    plt.show()


# 3. 定义函数, 用于实现: 逻辑回归模型的训练和评估.
def dm03_逻辑回归模型训练评估():
    # 1. 读取数据.
    data = pd.read_csv('./data/churn.csv')

    # 2. 对上述的数据做 热编码处理.
    data = pd.get_dummies(data)

    # 3. 删除列.
    data.drop(['gender_Male', 'Churn_No'], axis=1, inplace=True)

    # 4. 修改列名.
    data.rename(columns={'Churn_Yes': 'flag'}, inplace=True)

    # 5. 提取 特征列 和 标签列.
    x = data[['Contract_Month', 'PaymentElectronic', 'internet_other']]
    y = data['flag']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=22)

    # 7. 创建逻辑回归模型, 并训练.
    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)

    # 8. 模型预测.
    y_predict = estimator.predict(x_test)
    print(f'预测值为: {y_predict}')

    # 9. 模型评估.
    # 9.1 准确率.
    print(f'准确率: {estimator.score(x_test, y_test)}')
    print(f'准确率: {accuracy_score(y_test, y_predict)}')
    print('-' * 22)
    # 9.2 精确率.
    print(f'精确率: {precision_score(y_test, y_predict)}')
    print('-' * 22)
    # 9.3 召回率.
    print(f'召回率: {recall_score(y_test, y_predict)}')
    print('-' * 22)
    # 9.4 F1值
    print(f'F1值: {f1_score(y_test, y_predict)}')
    print('-' * 22)
    # 9.5 roc曲线
    print(f'roc曲线: {roc_auc_score(y_test, y_predict)}')
    print('-' * 22)
    # 9.6 分类评估报告
    # macro: 宏平均, 忽略样本数量差异.
    # weighted: 样本权重平均, 考虑样本数量差异.
    print(f'分类评估报告: {classification_report(y_test, y_predict)}')


if __name__ == '__main__':
    # dm01_数据预处理()
    # dm02_会员流失可视化情况()
    dm03_逻辑回归模型训练评估()
