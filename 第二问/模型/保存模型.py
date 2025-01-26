import pandas as pd
import statsmodels.api as sm
import os
import pickle

# 定义数据路径
data_path = r"D:\桌面\2025美国数学建模\数据\名帅效应\Sport_NOC_coach"

# 定义输出目录以保存模型
output_model_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\模型结果"
os.makedirs(output_model_dir, exist_ok=True)  # 确保输出目录存在

# 读取数据
def load_data(folder_path):
    all_files = os.listdir(folder_path)
    df_list = []
    for file in all_files:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

# 加载数据
df = load_data(data_path)

# 数据准备
df = df.sort_values(by=["NOC", "Sport", "Year"])
df = df.dropna()  # 删除缺失值

# 创建滞后变量
def create_lag_variables(df, lags):
    for lag in lags:
        df[f"coach_lag{lag}"] = df.groupby(["NOC", "Sport"])["score"].shift(lag)
    return df

# 创建滞后变量
df = create_lag_variables(df, lags=[1, 2, 3, 4, 5])

# 删除因滞后变量引入的缺失值
df = df.dropna()

# 定义自变量和因变量
control_vars = ["athletes_number", "Year"] + [col for col in df.columns if col.startswith("NOC_") or col.startswith("Sport_")]
short_term_vars = ["coach_lag1", "coach_lag2"] + control_vars
long_term_vars = ["coach_lag3", "coach_lag4", "coach_lag5"] + control_vars

# 训练短期模型
X_short = df[short_term_vars]
X_short = sm.add_constant(X_short)  # 添加截距项
y = df["score"]
short_term_model = sm.OLS(y, X_short).fit()

# 训练长期模型
X_long = df[long_term_vars]
X_long = sm.add_constant(X_long)  # 添加截距项
long_term_model = sm.OLS(y, X_long).fit()

# 保存短期模型
short_term_model_path = os.path.join(output_model_dir, "short_term_model.pkl")
with open(short_term_model_path, 'wb') as f:
    pickle.dump(short_term_model, f)
print(f"短期模型已保存到 {short_term_model_path}")

# 保存长期模型
long_term_model_path = os.path.join(output_model_dir, "long_term_model.pkl")
with open(long_term_model_path, 'wb') as f:
    pickle.dump(long_term_model, f)
print(f"长期模型已保存到 {long_term_model_path}")
