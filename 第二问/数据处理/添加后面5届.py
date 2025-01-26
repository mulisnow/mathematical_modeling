import pandas as pd
import os

# 定义数据路径
data_folder = r"D:\桌面\2025美国数学建模\数据\名帅效应\三个国家"
output_folder = os.path.join(data_folder, "modified_data")
os.makedirs(output_folder, exist_ok=True)  # 确保输出目录存在

# 定义要添加的年份
years_to_add = [2028, 2032, 2036, 2040, 2044, 2048]

# 遍历数据文件
for filename in os.listdir(data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_folder, filename)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 获取2024年的athletes_number值
        athletes_number_2024 = df.loc[df['Year'] == 2024, 'athletes_number'].values[0] if not df[
            df['Year'] == 2024].empty else 0

        # 为每个新年份创建新行
        new_rows = []
        for year in years_to_add:
            new_row = {
                'NOC': df['NOC'].values[0],  # 假设NOC在文件中是相同的
                'Sport': df['Sport'].values[0],  # 假设Sport在文件中是相同的
                'Year': year,
                'gold_number': 0,
                'silver_number': 0,
                'bronze_number': 0,
                'total_number': 0,
                'athletes_number': athletes_number_2024,
                'score': 0,
                'coach': 1
            }
            new_rows.append(new_row)

        # 将新行添加到DataFrame
        new_rows_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_rows_df], ignore_index=True)

        # 保存修改后的数据
        output_file_path = os.path.join(output_folder, filename)
        df.to_csv(output_file_path, index=False)
        print(f"修改后的数据已保存到 {output_file_path}")

print("所有文件处理完成。")