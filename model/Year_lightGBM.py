import os
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load  # 导入joblib库
import matplotlib.pyplot as plt

# 读取数据文件所在目录
data_dir = "D:/桌面/2025美国数学建模/数据/特征工程"
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]

# 合并所有CSV数据
all_data = pd.DataFrame()

for file in data_files:
    df = pd.read_csv(file)
    #df = df[df['Year'].astype(int) >= 1896 ]  # 只使用2000年及以后的数据
    all_data = pd.concat([all_data, df], ignore_index=True)

# 处理缺失值
all_data = all_data.fillna(0)

# 确保 'NOC' 列是字符串类型
all_data['NOC'] = all_data['NOC'].astype(str)
#all_data['Host']=all_data['Host']*1000
# 提取特征
features = all_data[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                     'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                     'total_number_previous', 'Host']].copy()
features['Host']=features['Host']*10000
c=features['Host']
for value in c:
    if value > 1:
        # 执行某些操作
        print(value)
# 对分类特征进行编码
le_noc = LabelEncoder()
le_sport = LabelEncoder()
le_event = LabelEncoder()

features['NOC'] = le_noc.fit_transform(features['NOC'])
features['Sport'] = le_sport.fit_transform(features['Sport'])
features['Event'] = le_event.fit_transform(features['Event'])

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, all_data[['Gold', 'Silver', 'Bronze', 'Total']],
                                                    test_size=0.2, random_state=42)

# 分别训练每个目标变量
model_gold = lgb.LGBMRegressor(random_state=42, n_jobs=-1)
model_silver = lgb.LGBMRegressor(random_state=42, n_jobs=-1)
model_bronze = lgb.LGBMRegressor(random_state=42, n_jobs=-1)
model_total = lgb.LGBMRegressor(random_state=42, n_jobs=-1)

# 训练每个模型
model_gold.fit(X_train, y_train['Gold'])
model_silver.fit(X_train, y_train['Silver'])
model_bronze.fit(X_train, y_train['Bronze'])
model_total.fit(X_train, y_train['Total'])

# 保存模型
model_dir = "D:/桌面/2025美国数学建模/模型/1896"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

dump(model_gold, os.path.join(model_dir, 'model_gold.joblib'))
dump(model_silver, os.path.join(model_dir, 'model_silver.joblib'))
dump(model_bronze, os.path.join(model_dir, 'model_bronze.joblib'))
dump(model_total, os.path.join(model_dir, 'model_total.joblib'))

# 保存LabelEncoder
dump(le_noc, os.path.join(model_dir, 'le_noc.joblib'))
dump(le_sport, os.path.join(model_dir, 'le_sport.joblib'))
dump(le_event, os.path.join(model_dir, 'le_event.joblib'))

# 训练模型后，获取特征重要性
importance = model_gold.feature_importances_

# 创建特征名称列表
feature_names = features.columns.tolist()

# 绘制特征重要性图
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importance, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Feature Importance for Gold Medal Prediction')
plt.savefig(r"D:\桌面\2025美国数学建模\模型\图表\feature_importance.png")  # 保存特征重要性图
plt.show()

# 预测测试集
y_pred_gold = model_gold.predict(X_test)

# 绘制预测结果与实际结果的对比图
plt.figure(figsize=(10, 6))
plt.scatter(y_test['Gold'], y_pred_gold, alpha=0.5)
plt.plot([y_test['Gold'].min(), y_test['Gold'].max()], [y_test['Gold'].min(), y_test['Gold'].max()], 'r--')
plt.xlabel('Actual Gold Medals')
plt.ylabel('Predicted Gold Medals')
plt.title('Actual vs Predicted Gold Medals')
plt.savefig(r"D:\桌面\2025美国数学建模\模型\图表\actual_vs_predicted_gold.png")  # 保存预测结果对比图
plt.show()
