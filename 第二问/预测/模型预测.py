import pandas as pd
import pickle
import os
import statsmodels.api as sm

# 定义模型路径
output_model_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\模型结果"
short_term_model_path = os.path.join(output_model_dir, "short_term_model.pkl")
long_term_model_path = os.path.join(output_model_dir, "long_term_model.pkl")

# 加载训练好的模型
with open(short_term_model_path, 'rb') as f:
    short_term_model = pickle.load(f)
with open(long_term_model_path, 'rb') as f:
    long_term_model = pickle.load(f)

# 定义新数据路径和输出路径
new_data_folder = r"D:\桌面\2025美国数学建模\数据\名帅效应\三个国家\modified_data\with_lags"
output_prediction_folder = r"D:\桌面\2025美国数学建模\数据\名帅效应\预测结果"
os.makedirs(output_prediction_folder, exist_ok=True)  # 确保输出目录存在

# 遍历新数据文件
for filename in os.listdir(new_data_folder):
    if filename.endswith(".csv"):
        new_data_path = os.path.join(new_data_folder, filename)
        new_data = pd.read_csv(new_data_path)

        # 检查新数据列名
        print(f"处理文件: {filename}")
        print("新数据列名：", new_data.columns)

        # 定义自变量
        control_vars = ["athletes_number", "Year"] + [col for col in new_data.columns if col.startswith("NOC_") or col.startswith("Sport_")]
        short_term_vars = ["coach_lag1", "coach_lag2"] + control_vars
        long_term_vars = ["coach_lag3", "coach_lag4", "coach_lag5"] + control_vars

        # 检查新数据是否包含所有自变量
        missing_vars_short = set(short_term_vars) - set(new_data.columns)
        missing_vars_long = set(long_term_vars) - set(new_data.columns)
        if missing_vars_short:
            print("短期模型缺失变量：", missing_vars_short)
            continue  # 跳过此文件
        if missing_vars_long:
            print("长期模型缺失变量：", missing_vars_long)
            continue  # 跳过此文件

        # 添加截距项
        X_short_new = sm.add_constant(new_data[short_term_vars])
        X_long_new = sm.add_constant(new_data[long_term_vars])

        # 使用模型进行预测
        short_term_predictions = short_term_model.predict(X_short_new)
        long_term_predictions = long_term_model.predict(X_long_new)

        # 将预测结果添加到新数据中
        new_data["short_term_predicted_score"] = short_term_predictions
        new_data["long_term_predicted_score"] = long_term_predictions

        # 计算引入名帅后的增长
        new_data["short_term_growth"] = new_data["short_term_predicted_score"] - new_data["score"]
        new_data["long_term_growth"] = new_data["long_term_predicted_score"] - new_data["score"]

        # 输出预测结果
        output_prediction_path = os.path.join(output_prediction_folder, f"{filename.replace('.csv', '_predictions.csv')}")
        new_data.to_csv(output_prediction_path, index=False)
        print(f"预测结果已保存到 {output_prediction_path}")

print("所有文件处理完成。")