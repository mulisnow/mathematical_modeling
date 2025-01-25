import pandas as pd
import os

def load_and_extend_features(input_file, output_directory, n):
    # 读取数据文件
    medal_data = pd.read_csv(input_file)
    
    # 初始化一个空的数据框
    all_features = pd.DataFrame()

    # 选择特征
    features = select_features(medal_data, n)
    
    # 按年份分组并保存
    for year, group in features.groupby('Year'):
        year_file_path = os.path.join(output_directory, f"features_{year}.csv")
        group.to_csv(year_file_path, index=False)
        print(f"特征数据已保存到: {year_file_path}")

def select_features(medal_data, n):
    # 选择基本特征
    features = medal_data[['Year', 'NOC', 'Host', 'Sport', 'Event']]
    
    # 计算 Total Events
    total_events = medal_data.groupby(['Year', 'NOC']).size().reset_index(name='Total Events')
    features = features.merge(total_events, on=['Year', 'NOC'], how='left')
    
    # 计算 Previous Medals
    previous_medals = medal_data.groupby(['NOC']).agg(
        Previous_Medals=('total_number', lambda x: x.tail(n).sum())
    ).reset_index()
    features = features.merge(previous_medals, on='NOC', how='left')
    
    # 计算 Home Advantage
    features['Home Advantage'] = features.apply(lambda row: 1 if row['NOC'] == row['Host'] else 0, axis=1)
    
    # 处理缺失值
    features.fillna(0, inplace=True)
    
    return features

# 示例调用
if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"
    output_directory = r"D:\桌面\2025美国数学建模\数据\特征工程"
    n = 3  # 过去的奥运会数量
    load_and_extend_features(input_file, output_directory, n)
