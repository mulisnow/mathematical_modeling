import os
import numpy as np
from joblib import load
import lightgbm as lgb
from sklearn.metrics import mean_squared_error, r2_score

# 读取保存的模型
model_dir = "D:/桌面/2025美国数学建模/模型/1896"
model_gold = load(os.path.join(model_dir, 'model_gold.joblib'))
model_silver = load(os.path.join(model_dir, 'model_silver.joblib'))
model_bronze = load(os.path.join(model_dir, 'model_bronze.joblib'))
model_total = load(os.path.join(model_dir, 'model_total.joblib'))

# 假设你有一个新的特征集 X_new 用于预测
# X_new = ...  # 这里需要定义你的新特征集

# 进行预测
y_pred_gold = model_gold.predict(X_new)
y_pred_silver = model_silver.predict(X_new)
y_pred_bronze = model_bronze.predict(X_new)
y_pred_total = model_total.predict(X_new)

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

# 打印预测区间
print("Gold Medal Prediction Interval:")
print(f"Lower Bound: {lower_bound_gold}, Upper Bound: {upper_bound_gold}")

print("Silver Medal Prediction Interval:")
print(f"Lower Bound: {lower_bound_silver}, Upper Bound: {upper_bound_silver}")

print("Bronze Medal Prediction Interval:")
print(f"Lower Bound: {lower_bound_bronze}, Upper Bound: {upper_bound_bronze}")

print("Total Medal Prediction Interval:")
print(f"Lower Bound: {lower_bound_total}, Upper Bound: {upper_bound_total}")