import os
import pandas as pd

def process_sport_data(input_file, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取数据
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # 检查是否包含必要的列
    if 'Sport' not in data.columns or 'athletes_number' not in data.columns or 'Total Events' not in data.columns or 'NOC' not in data.columns:
        print("数据中缺少必要的列，无法处理。")
        return

    # 删除包含 Weightlifting 和 Boxing 的行
    deleted_data = data[data['Sport'].str.contains('Weightlifting|Boxing', case=False, na=False)]
    data = data[~data['Sport'].str.contains('Weightlifting|Boxing', case=False, na=False)]

    # 查看删除的行的 athletes_number 数量
    athletes_count = deleted_data['athletes_number'].sum()
    print(f"删除的行的总运动员数量: {athletes_count}")

    # 更新 Total Events 和 Host 列
    for noc in data['NOC'].unique():
        data.loc[data['NOC'] == noc, 'Total Events'] -= 1  # 减去1

    # 设置 Host 列
    data['Host'] = 0  # 默认值为0
    data.loc[data['NOC'] == 'USA', 'Host'] = 1  # NOC为USA的Host值改为1

    # 保存删除的数据
    deleted_data.to_csv(os.path.join(output_dir, 'deleted_weightlifting_boxing.csv'), index=False, encoding='utf-8-sig')
    print(f"删除的数据已保存到: {os.path.join(output_dir, 'deleted_weightlifting_boxing.csv')}")

    # 保存处理后的数据
    processed_file_path = os.path.join(output_dir, 'processed_feature_analysis_2024.csv')
    data.to_csv(processed_file_path, index=False, encoding='utf-8-sig')
    print(f"处理后的数据已保存到: {processed_file_path}")

if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\数据\特征工程\feature_analysis_2024.csv"
    output_directory = r"D:\桌面\2025美国数学建模\数据\处理结果"
    process_sport_data(input_file, output_directory) 