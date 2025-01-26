import pandas as pd
import os

# 定义数据路径
data_folder = r"D:\桌面\2025美国数学建模\数据\名帅效应\三个国家"

# 定义输出目录
output_folder = os.path.join(data_folder, "with_lags")
os.makedirs(output_folder, exist_ok=True)  # 确保输出目录存在


# 读取所有数据文件
def load_all_data(folder_path):
    all_files = os.listdir(folder_path)
    df_list = []
    for file in all_files:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            df_list.append(df)
    return df_list


# 计算滞后变量
def calculate_lag_variables(df):
    # 按NOC和Sport分组，计算滞后变量
    df = df.sort_values(by=["NOC", "Sport", "Year"])
    for lag in [1, 2, 3, 4, 5]:
        df[f"coach_lag{lag}"] = df.groupby(["NOC", "Sport"])["coach"].shift(lag)
    return df


# 处理所有数据文件
def process_all_files(folder_path, output_folder):
    all_files = os.listdir(folder_path)
    for file in all_files:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # 计算滞后变量
            df_with_lags = calculate_lag_variables(df)

            # 保存副本
            output_file_path = os.path.join(output_folder, file.replace(".csv", "_with_lags.csv"))
            df_with_lags.to_csv(output_file_path, index=False)
            print(f"处理后的数据已保存到 {output_file_path}")


# 处理所有文件
process_all_files(data_folder, output_folder)