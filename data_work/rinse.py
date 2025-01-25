import pandas as pd
import os

# 读取CSV文件
file_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"
data = pd.read_csv(file_path)

# 显示原始数据的前几行
print("原始数据:")
print(data.head())

# 创建一个目录来保存删除的数据
deleted_data_dir = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\deleted_data"
os.makedirs(deleted_data_dir, exist_ok=True)

# 记录删除的重复行
duplicates = data[data.duplicated(keep=False)]
data = data.drop_duplicates()

# 保存重复行到CSV
if not duplicates.empty:
    duplicates_file_path = os.path.join(deleted_data_dir, "deleted_duplicates.csv")
    duplicates.to_csv(duplicates_file_path, index=False, encoding='utf-8')
    print(f"删除的重复行已保存到: {duplicates_file_path}")

# 记录缺失值的行
missing_values = data[data.isnull().any(axis=1)]
data = data.dropna()

# 保存缺失值行到CSV
if not missing_values.empty:
    missing_values_file_path = os.path.join(deleted_data_dir, "deleted_missing_values.csv")
    missing_values.to_csv(missing_values_file_path, index=False, encoding='utf-8')
    print(f"删除的缺失值行已保存到: {missing_values_file_path}")

# 重置索引
data.reset_index(drop=True, inplace=True)

# 显示清洗后的数据
print("\n清洗后的数据:")
print(data.head())

# 可选：将清洗后的数据保存到新的CSV文件
cleaned_file_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\cleaned_summerOly_athletes.csv"
data.to_csv(cleaned_file_path, index=False, encoding='utf-8')
print(f"\n清洗后的数据已保存到: {cleaned_file_path}")