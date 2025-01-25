import pandas as pd
import os
import matplotlib.pyplot as plt

def analyze_features_by_file(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的每个文件
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.csv'):
            year_data = pd.read_csv(os.path.join(input_dir, filename))

            # 检查必要的列
            required_columns = ['NOC', 'Sport', 'Event', 'Medal']
            if not all(col in year_data.columns for col in required_columns):
                print(f"错误：文件 {filename} 中缺少必要的列")
                continue

            # 计算每个国家在每个运动项目中的运动员数量和奖牌数量
            feature_data = year_data.groupby(['NOC', 'Sport', 'Event']).agg(
                athletes_number=('Name', 'nunique'),  # 计算运动员数量
                gold_number=('Medal', lambda x: (x == 'Gold').sum()),  # 计算金牌数量
                silver_number=('Medal', lambda x: (x == 'Silver').sum()),  # 计算银牌数量
                bronze_number=('Medal', lambda x: (x == 'Bronze').sum()),  # 计算铜牌数量
            ).reset_index()

            # 计算总奖牌数量
            feature_data['total_number'] = feature_data['gold_number'] + feature_data['silver_number'] + feature_data['bronze_number']

            # 计算该国在这一年奥运会中参加的总项目数
            feature_data['Total Events'] = feature_data.groupby('NOC')['Event'].transform('nunique')

            # 添加年份列
            feature_data['Year'] = os.path.splitext(filename)[0]  # 从文件名中提取年份

            # 保存特征数据
            output_file = os.path.join(output_dir, f"feature_analysis_{feature_data['Year'].iloc[0]}.csv")
            feature_data.to_csv(output_file, index=False, encoding='utf-8')  # 确保字符完整保存

    # 计算 Previous Medals
    calculate_previous_medals(output_dir)

def calculate_previous_medals(output_dir):
    # 获取所有特征文件并按年份排序
    feature_files = sorted([f for f in os.listdir(output_dir) if f.startswith("feature_analysis_") and f.endswith('.csv')])

    for i, filename in enumerate(feature_files):
        feature_data = pd.read_csv(os.path.join(output_dir, filename))

        if i > 0:  # 确保有前一届数据
            previous_filename = feature_files[i - 1]
            previous_data = pd.read_csv(os.path.join(output_dir, previous_filename))

            # 合并前一届的奖牌数据
            feature_data = feature_data.merge(
                previous_data[['NOC', 'Sport', 'Event', 'gold_number', 'silver_number', 'bronze_number', 'total_number']],
                on=['NOC', 'Sport', 'Event'],
                how='left',
                suffixes=('', '_previous')
            )

            # 填充缺失值为0
            feature_data.fillna({'gold_number_previous': 0, 'silver_number_previous': 0, 'bronze_number_previous': 0, 'total_number_previous': 0}, inplace=True)

        else:
            # 如果没有前一届数据，初始化为0
            feature_data['gold_number_previous'] = 0
            feature_data['silver_number_previous'] = 0
            feature_data['bronze_number_previous'] = 0
            feature_data['total_number_previous'] = 0

        # 保存更新后的特征数据
        feature_data.to_csv(os.path.join(output_dir, filename), index=False, encoding='utf-8')

def plot_medal_distribution(features):
    # 示例分析：绘制奖牌分布
    medal_counts = features.groupby('NOC')['total_number'].sum().reset_index()
    plt.bar(medal_counts['NOC'], medal_counts['total_number'])
    plt.xlabel('Country')
    plt.ylabel('Total Medals')
    plt.title('Total Medals by Country')
    plt.show()

if __name__ == "__main__":
    input_dir = "D:/桌面/2025美国数学建模/数据/年份国家运动员奖牌"  # 输入目录
    output_dir = "D:/桌面/2025美国数学建模/数据/特征工程"  # 输出目录
    analyze_features_by_file(input_dir, output_dir)