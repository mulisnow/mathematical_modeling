import pandas as pd
import os

def classify_data(input_path, output_dir):
    # 读取数据
    try:
        data = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_path}")
        return

    # 检查 NOC 列
    print(data['NOC'].unique())  # 打印 NOC 列的唯一值
    print(data['NOC'].isnull().sum())  # 打印 NOC 列的缺失值数量

    # 去除国家名称的前后空格和不可见字符
    data['NOC'] = data['NOC'].str.replace('\xa0', '', regex=False)  # 去除不可见字符
    data['NOC'] = data['NOC'].str.strip()  # 去除前后空格

    # 按 NOC 列分类
    grouped = data.groupby('NOC')

    # 输出每个国家的记录数
    print("\n每个国家的记录数：")
    for name, group in grouped:
        print(f"{name}: {len(group)}")

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存分类后的数据
    for name, group in grouped:
        output_file = os.path.join(output_dir, f"{name}.csv")
        group.to_csv(output_file, index=False, encoding='utf-8')  # 确保字符完整保存

if __name__ == "__main__":
    input_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_medal_counts.csv"  # 输入文件路径
    output_dir = r"D:\桌面\2025美国数学建模\数据\国家历史奖牌"  # 输出目录
    classify_data(input_path, output_dir)
