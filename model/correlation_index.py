import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 读取数据文件所在目录
data_dir = "D:/桌面/2025美国数学建模/数据/特征工程"
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]

# 合并所有CSV数据
all_data = pd.DataFrame()

for file in data_files:
    df = pd.read_csv(file)
    df = df[df['Year'] >= 1896]  # 只使用1896年及以后的数据
    all_data = pd.concat([all_data, df], ignore_index=True)

# 处理缺失值
all_data = all_data.fillna(0)

# 确保 'NOC' 列是字符串类型
all_data['NOC'] = all_data['NOC'].astype(str)

# 提取特征
features = all_data[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                     'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                     'total_number_previous', 'Host']].copy()
features['Host'] = features['Host'] * 1

# 对分类特征进行编码
le_noc = LabelEncoder()
le_sport = LabelEncoder()
le_event = LabelEncoder()

features['NOC'] = le_noc.fit_transform(features['NOC'])
features['Sport'] = le_sport.fit_transform(features['Sport'])
features['Event'] = le_event.fit_transform(features['Event'])

# 提取目标变量
targets = all_data[['Gold', 'Silver', 'Bronze', 'Total']]

# 计算相关系数
combined_data = pd.concat([features, targets], axis=1)
correlation_matrix = combined_data.corr()

# 提取特征与目标变量的相关系数
target_correlations = correlation_matrix.loc[features.columns, targets.columns]

print("特征与目标变量的相关系数：")
print(target_correlations)