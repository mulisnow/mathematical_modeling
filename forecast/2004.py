import os
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder

# 定义数据文件路径和输出目录
prediction_data_file = r"D:\桌面\2025美国数学建模\数据\特征工程\feature_analysis_2004.csv"
output_dir = r"D:\桌面\2025美国数学建模\结果"
model_dir = r"D:\桌面\2025美国数学建模\模型"

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取预测数据
df_2004 = pd.read_csv(prediction_data_file)

# 保存原始的 NOC 列
original_noc = df_2004['NOC'].astype(str)

# 确保 'NOC' 列是字符串类型
df_2004['NOC'] = df_2004['NOC'].astype(str)

# 加载LabelEncoder
le_noc = load(os.path.join(model_dir, 'le_noc.joblib'))
le_sport = load(os.path.join(model_dir, 'le_sport.joblib'))
le_event = load(os.path.join(model_dir, 'le_event.joblib'))

# 对分类特征进行编码
df_2004['NOC'] = le_noc.transform(df_2004['NOC'])
df_2004['Sport'] = le_sport.transform(df_2004['Sport'])
df_2004['Event'] = le_event.transform(df_2004['Event'])

# 选择预测特征
features_2004 = df_2004[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                        'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                        'total_number_previous', 'Host']].copy()

# 加载训练好的模型
model_gold = load(os.path.join(model_dir, 'model_gold.joblib'))
model_silver = load(os.path.join(model_dir, 'model_silver.joblib'))
model_bronze = load(os.path.join(model_dir, 'model_bronze.joblib'))
model_total = load(os.path.join(model_dir, 'model_total.joblib'))

# 使用训练好的模型进行预测
predictions_gold = model_gold.predict(features_2004)
predictions_silver = model_silver.predict(features_2004)
predictions_bronze = model_bronze.predict(features_2004)
predictions_total = model_total.predict(features_2004)

# 生成结果 DataFrame
results = pd.DataFrame({
    'Gold': predictions_gold,
    'Silver': predictions_silver,
    'Bronze': predictions_bronze,
    'Total': predictions_total,
    'NOC': original_noc  # 使用原始的 NOC 列
})

# 保存结果到指定路径
output_file = os.path.join(output_dir, "predictions_2004.csv")
results.to_csv(output_file, index=False)

print(f"预测结果已保存到 {output_file}")