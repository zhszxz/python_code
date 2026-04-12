"""
案例: 演示网格搜索 和 交叉验证.

交叉验证解释:
   把数据分成多组，让组数据都“轮流当测试集”,训练+测试,让模型准确率更可信

网格搜索:
    目的:
        寻找最优超参数.
    原理:
        对于超参所有可能的组合,进行 交叉验证, 获取到 最优超参组合.
"""
# 导入工具包
from sklearn.datasets import load_iris  # 加载鸢尾花测试集的.
from sklearn.model_selection import train_test_split, GridSearchCV  # 分割训练集和测试集的, 寻找最优超参的(网格搜索 ＋ 交叉验证).
from sklearn.preprocessing import StandardScaler  # 数据标准化的
from sklearn.neighbors import KNeighborsClassifier  # KNN算法 分类对象
from sklearn.metrics import accuracy_score  # 模型评估的, 计算模型预测的准确率

# 1. 加载鸢尾花数据集.
iris_data = load_iris()

# 2. 数据预处理, 这里是: 切分训练集和测试集, 比例: 8:2
x_train, x_test, y_train, y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.2, random_state=22)

# 3. 特征工程 -> 特征预处理 -> 标准化.
# 3.1 创建标准化对象.
transfer = StandardScaler()
# 3.2 对训练集和测试集的特征数据进行标准化.
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)

# 4. 模型训练.
# 4.1 创建 KNN分类对象.
estimator = KNeighborsClassifier()
# 4.2 定义字典, 记录每个超参可能的取值.
param_dict = {'n_neighbors': [i for i in range(1, 11)]}
# 4.3 创建 GridSearchCV对象 -> 寻找最优超参, 使用网格搜索 + 交叉验证方式
# 参1: 要计算最优超参的模型对象
# 参2: 该模型超参可能出现的值
# 参3: 交叉验证的折数, 这里的4表示: 将训练集划为四份轮流做测试集,每个超参组合, 都会进行4次验证. 共计是 4 * 10 = 40次.
# 返回值 estimator -> 处理后的模型对象.
estimator = GridSearchCV(estimator, param_dict, cv=4)
# 4.4 具体的模型训练动作.
estimator.fit(x_train, y_train)
# 4.5 打印最优超参组合.
print(f'最优评分: {estimator.best_score_}')  # 0.9666666666666668
print(f'最优超参组合: {estimator.best_params_}')  # {'n_neighbors': 3}
print(f'最优的估计器对象: {estimator.best_estimator_}')  # KNeighborsClassifier(n_neighbors=3)
print(f'具体的交叉验证结果: {estimator.cv_results_}')

# 5. 模型评估.
# 5.1 获取最优超参的 模型对象.
# estimator = estimator.best_estimator_                 # 获取最优的模型对象.
estimator = KNeighborsClassifier(n_neighbors=3)
# 5.2 模型训练.
estimator.fit(x_train, y_train)
# 5.3 模型预测.
y_pre = estimator.predict(x_test)
# 5.4 模型评估.
# 参1: 测试集.   参2: 预测集
print(f'准确率: {accuracy_score(y_test, y_pre)}')  # 0.9666666666666667
