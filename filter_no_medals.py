import os
import pandas as pd

def filter_no_medals(noc_file, predictions_file, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取 NOC 文件
    noc_data = pd.read_csv(noc_file, encoding='utf-8-sig')
    noc_values = noc_data['NOC'].unique()  # 提取唯一的 NOC 值
    print(f"找到 {len(noc_values)} 个 NOC 值。")

    # 读取预测结果文件
    predictions_data = pd.read_csv(predictions_file, encoding='utf-8-sig')

    # 筛选出对应的 NOC 行
    filtered_data = predictions_data[predictions_data['NOC'].isin(noc_values)]

    # 保存结果
    output_file_path = os.path.join(output_dir, 'no_medals_predictions.csv')
    filtered_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')
    print(f"筛选结果已保存到: {output_file_path}")

if __name__ == "__main__":
    noc_file = r"D:\桌面\2025美国数学建模\数据\一次都没获奖\noc_with_all_zero_total_number.csv"
    predictions_file = r"D:\桌面\2025美国数学建模\结果\averaged_predictions_2028.csv"
    output_directory = r"D:\桌面\2025美国数学建模\数据\一次都没获奖"
    filter_no_medals(noc_file, predictions_file, output_directory) 