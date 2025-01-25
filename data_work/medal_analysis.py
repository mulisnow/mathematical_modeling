import pandas as pd
import os

def analyze_medal_data(input_file, output_dir):
    # 读取数据
    try:
        data = pd.read_csv(input_file, encoding='utf-8')
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file}")
        return

    # 检查必要的列
    required_columns = ['Year', 'NOC', 'Sport', 'Event', 'Gold', 'Silver', 'Bronze']
    if not all(col in data.columns for col in required_columns):
        print("错误：数据中缺少必要的列")
        return

    # 计算每个国家在特定年份的总奖牌数和参与的赛事数
    medal_summary = data.groupby(['Year', 'NOC']).agg(
        total_gold=('Gold', 'sum'),
        total_silver=('Silver', 'sum'),
        total_bronze=('Bronze', 'sum'),
        total_events=('Event', 'nunique')  # 计算参与的赛事数量
    ).reset_index()

    # 计算总奖牌数
    medal_summary['total_medals'] = medal_summary['total_gold'] + medal_summary['total_silver'] + medal_summary['total_bronze']

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 保存结果到CSV文件
    output_file_path = os.path.join(output_dir, 'medal_analysis_summary.csv')
    medal_summary.to_csv(output_file_path, index=False, encoding='utf-8-sig')
    print(f"奖牌分析结果已保存到: {output_file_path}")

if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\数据\项目国家运动员奖牌\event_medal_summary.csv"
    output_directory = r"D:\桌面\2025美国数学建模\数据\奖牌分析"
    analyze_medal_data(input_file, output_directory) 