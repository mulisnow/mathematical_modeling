import pandas as pd
import os

def sanitize_filename(filename):
    # 替换非法字符
    return filename.replace('/', '_').replace('\\', '_').replace(':', '_')

def analyze_event_medals(input_file, output_dir):
    # 读取数据
    try:
        data = pd.read_csv(input_file, encoding='utf-8')
    except FileNotFoundError:
        print(f"错误：未找到文件 {input_file}")
        return

    # 检查必要的列
    required_columns = ['Year', 'NOC', 'Event', 'Sport', 'Medal']
    if not all(col in data.columns for col in required_columns):
        print("错误：数据中缺少必要的列")
        return

    # 按 Year、Event、NOC 和 Sport 分组，计算所需的统计数据
    medal_summary = data.groupby(['Year', 'Event', 'NOC', 'Sport']).agg(
        gold_number=('Medal', lambda x: (x == 'Gold').sum()),
        silver_number=('Medal', lambda x: (x == 'Silver').sum()),
        bronze_number=('Medal', lambda x: (x == 'Bronze').sum()),
        no_medal_number=('Medal', lambda x: (x == 'No medal').sum()),
        total_number=('Medal', lambda x: len(x))  # 总数为所有奖牌的数量
    ).reset_index()

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 为每个事件创建单独的文件
    for (sport, event), group in medal_summary.groupby(['Sport', 'Event']):
        # 创建文件名
        sanitized_sport = sanitize_filename(sport)
        sanitized_event = sanitize_filename(event)
        file_name = f"{sanitized_sport}_{sanitized_event}.csv"
        output_file_path = os.path.join(output_dir, file_name)
        
        # 保存每个事件的统计数据到CSV文件
        group.to_csv(output_file_path, index=False, encoding='utf-8-sig')  # 使用 'utf-8-sig' 以避免乱码
        print(f"结果已保存到: {output_file_path}")

if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"
    output_directory = r"D:\桌面\2025美国数学建模\数据\项目国家运动员奖牌"
    analyze_event_medals(input_file, output_directory)