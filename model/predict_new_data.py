import os
import pandas as pd
import numpy as np
from joblib import load
import lightgbm as lgb

# 读取保存的模型
model_dir = "D:/桌面/2025美国数学建模/模型/1896"
model_gold = load(os.path.join(model_dir, 'model_gold.joblib'))
model_silver = load(os.path.join(model_dir, 'model_silver.joblib'))
model_bronze = load(os.path.join(model_dir, 'model_bronze.joblib'))
model_total = load(os.path.join(model_dir, 'model_total.joblib'))

# 读取新的特征数据
data_path = "D:/桌面/2025美国数学建模/数据/预测/feature_analysis_2028.csv"
new_data = pd.read_csv(data_path)

# 预处理数据以匹配训练时的特征
# 确保 'NOC' 列是字符串类型
new_data['NOC'] = new_data['NOC'].astype(str)
original_noc = new_data['NOC'].copy()  # 保存原始的 NOC 字符串

# 对分类特征进行编码
le_noc = load(os.path.join(model_dir, 'le_noc.joblib'))
le_sport = load(os.path.join(model_dir, 'le_sport.joblib'))
le_event = load(os.path.join(model_dir, 'le_event.joblib'))

# 对 NOC, Sport 和 Event 进行编码
new_data['NOC'] = le_noc.transform(new_data['NOC'])
new_data['Sport'] = le_sport.transform(new_data['Sport'])
new_data['Event'] = le_event.transform(new_data['Event'])

# 提取特征，包括 NOC
features = new_data[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                     'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                     'total_number_previous', 'Host']]

# 进行预测
y_pred_gold = model_gold.predict(features)
y_pred_silver = model_silver.predict(features)
y_pred_bronze = model_bronze.predict(features)
y_pred_total = model_total.predict(features)

# 计算标准差
std_dev_gold = np.std(y_pred_gold)
std_dev_silver = np.std(y_pred_silver)
std_dev_bronze = np.std(y_pred_bronze)
std_dev_total = np.std(y_pred_total)

# 计算预测区间
confidence_interval = 1.96  # 95% 置信区间
lower_bound_gold = y_pred_gold - confidence_interval * std_dev_gold
upper_bound_gold = y_pred_gold + confidence_interval * std_dev_gold

lower_bound_silver = y_pred_silver - confidence_interval * std_dev_silver
upper_bound_silver = y_pred_silver + confidence_interval * std_dev_silver

lower_bound_bronze = y_pred_bronze - confidence_interval * std_dev_bronze
upper_bound_bronze = y_pred_bronze + confidence_interval * std_dev_bronze

lower_bound_total = y_pred_total - confidence_interval * std_dev_total
upper_bound_total = y_pred_total + confidence_interval * std_dev_total

# 创建结果数据框，包括原始 NOC
results = pd.DataFrame({
    'NOC': original_noc,  # Use original NOC strings
    'Predicted Gold Medals': y_pred_gold,
    'Gold Lower Bound': lower_bound_gold,
    'Gold Upper Bound': upper_bound_gold,
    'Predicted Silver Medals': y_pred_silver,
    'Silver Lower Bound': lower_bound_silver,
    'Silver Upper Bound': upper_bound_silver,
    'Predicted Bronze Medals': y_pred_bronze,
    'Bronze Lower Bound': lower_bound_bronze,
    'Bronze Upper Bound': upper_bound_bronze,
    'Predicted Total Medals': y_pred_total,
    'Total Lower Bound': lower_bound_total,
    'Total Upper Bound': upper_bound_total
})

# 输出结果到指定路径
output_dir = "D:/桌面/2025美国数学建模/结果/预测区间"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

results.to_csv(os.path.join(output_dir, 'predictions_with_intervals.csv'), index=False)

# 打印预测结果
print("Predictions and intervals saved to:", os.path.join(output_dir, 'predictions_with_intervals.csv')) 