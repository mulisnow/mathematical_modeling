import pandas as pd
import os

def classify_by_year(input_path, output_dir):
    # 读取数据
    try:
        data = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
        return

    # 检查 Year 列
    if 'Year' not in data.columns:
        print("错误：数据中未找到 'Year' 列")
        return

    # 对 NOC 列进行升序排序
    data.sort_values(by='NOC', ascending=True, inplace=True)

    # 按年份分类
    grouped = data.groupby('Year')

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存分类后的数据
    for year, group in grouped:
        output_file = os.path.join(output_dir, f"{year}.csv")
        group.to_csv(output_file, index=False, encoding='utf-8')  # 确保字符完整保存

if __name__ == "__main__":
    input_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"  # 输入文件路径
    output_dir = r"D:\桌面\2025美国数学建模\数据\年份国家运动员奖牌"  # 输出目录
    classify_by_year(input_path, output_dir)
