import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# 加载保存的模型
model_dir = "D:/桌面/2025美国数学建模/模型"
model_gold = joblib.load(os.path.join(model_dir, 'model_gold.pkl'))
model_silver = joblib.load(os.path.join(model_dir, 'model_silver.pkl'))
model_bronze = joblib.load(os.path.join(model_dir, 'model_bronze.pkl'))
model_total = joblib.load(os.path.join(model_dir, 'model_total.pkl'))

# 读取USA数据
usa_data_file = r"D:/桌面/2025美国数学建模/USA.csv"
df_usa = pd.read_csv(usa_data_file)

# 确保 'NOC' 列是字符串类型
df_usa['NOC'] = df_usa['NOC'].astype(str)

# 创建LabelEncoder对象
le_noc = LabelEncoder()
le_sport = LabelEncoder()
le_event = LabelEncoder()

# 对分类特征进行编码
df_usa['NOC'] = le_noc.fit_transform(df_usa['NOC'])
df_usa['Sport'] = le_sport.fit_transform(df_usa['Sport'])
df_usa['Event'] = le_event.fit_transform(df_usa['Event'])

# 提取预测特征
features_usa = df_usa[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                       'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                       'total_number_previous', 'Host']].copy()

# 使用训练好的模型进行预测
predictions_gold = model_gold.predict(features_usa)
predictions_silver = model_silver.predict(features_usa)
predictions_bronze = model_bronze.predict(features_usa)
predictions_total = model_total.predict(features_usa)

# 生成结果 DataFrame
results = pd.DataFrame({
    'Gold': predictions_gold,
    'Silver': predictions_silver,
    'Bronze': predictions_bronze,
    'Total': predictions_total,
    'NOC': df_usa['NOC']
})

# 确保文件夹路径存在
output_dir = "D:/桌面/2025美国数学建模/结果"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存结果到指定路径
output_file = os.path.join(output_dir, "predictions_usa.csv")
results.to_csv(output_file, index=False)

print(f"预测结果已保存到 {output_file}")
