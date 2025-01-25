import pandas as p
import os
def train_lightgbm_model(data):
    # 检查必要的列
    required_columns = ['Year', 'NOC', 'Sport', 'Event', 'gold_number', 'silver_number', 'bronze_number', 'no_medal_number', 'total_number']
    if not all(col in data.columns for col in required_columns):
        print("错误：数据中缺少必要的列")
        return

    # 统计每个NOC在每个Event中的金牌、银牌和铜牌数量
    medal_summary = data.groupby(['NOC', 'Event']).agg({
        'gold_number': 'sum',
        'silver_number': 'sum',
        'bronze_number': 'sum'
    }).reset_index()

    # 计算每个事件的加权得分
    medal_summary['importance_score'] = (medal_summary['gold_number'] * 3 +
                                          medal_summary['silver_number'] * 2 +
                                          medal_summary['bronze_number'] * 1)

    return medal_summary  # 返回包含重要性得分的汇总数据

def process_files_in_directory(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 存储所有NOC和Event的重要性
    all_medal_summaries = []

    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):  # 只处理CSV文件
            file_path = os.path.join(input_dir, filename)
            print(f"正在处理文件: {file_path}")
            data = pd.read_csv(file_path, encoding='utf-8-sig')
            medal_summary = train_lightgbm_model(data)
            if medal_summary is not None:
                all_medal_summaries.append(medal_summary)

    # 合并所有重要性数据
    if all_medal_summaries:
        combined_medal_summary = pd.concat(all_medal_summaries)

        # 按NOC分组并保存每个国家的事件重要性
        for noc, group in combined_medal_summary.groupby('NOC'):
            output_file_path = os.path.join(output_dir, f"{noc}_event_importance.csv")
            group[['Event', 'importance_score']].to_csv(output_file_path, index=False, encoding='utf-8-sig')
            print(f"{noc} 的事件重要性已保存到: {output_file_path}")

if __name__ == "__main__":
    input_directory = r"D:\桌面\2025美国数学建模\数据\项目国家运动员奖牌"
    output_directory = r"D:\桌面\2025美国数学建模\数据\重要程度"  # 输出目录
    process_files_in_directory(input_directory, output_directory)