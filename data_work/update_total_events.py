import pandas as pd
import os

def update_total_events(input_file, output_file):
    # 读取数据
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # 检查是否包含必要的列
    required_columns = ['NOC', 'Total Events', 'gold_number', 'silver_number', 'bronze_number', 
                        'total_number', 'gold_number_previous', 'silver_number_previous', 
                        'bronze_number_previous', 'total_number_previous', 'Year']
    
    if not all(col in data.columns for col in required_columns):
        print("数据中缺少必要的列，无法处理。")
        return

    # 更新 Year 列为 2028
    data['Year'] = 2028

    # 更新 Total Events
    data.loc[data['NOC'] == 'USA', 'Total Events'] += 5
    data.loc[data['NOC'] == 'FRA', 'Total Events'] += 1
    data.loc[data['NOC'] == 'GBR', 'Total Events'] += 3
    data.loc[data['NOC'] == 'CAN', 'Total Events'] += 4
    data.loc[data['NOC'] == 'HKG', 'Total Events'] += 1
    data.loc[data['NOC'] == 'AUT', 'Total Events'] += 1
    data.loc[data['NOC'] == 'CHN', 'Total Events'] += 2

    # 更新其他 NOC 的 Total Events
    nocs_add_1 = ['TPE', 'RSA', 'PUR', 'NED', 'NCA', 'MEX', 'ITA', 'ISR', 'GRE', 'ESP', 'CUB', 'AUS']
    data.loc[data['NOC'].isin(nocs_add_1), 'Total Events'] += 1

    nocs_add_3 = ['KOR', 'JPN', 'DOM']
    data.loc[data['NOC'].isin(nocs_add_3), 'Total Events'] += 2

    # 替换 old_number_previous 列
    data['gold_number_previous'] = data['gold_number']
    data['silver_number_previous'] = data['silver_number']
    data['bronze_number_previous'] = data['bronze_number']
    data['total_number_previous'] = data['total_number']

    # 保存更新后的数据
    data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"更新后的数据已保存到: {output_file}")

if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\数据\处理结果\processed_feature_analysis_2024.csv"
    output_file = r"D:\桌面\2025美国数学建模\数据\预测\feature_analysis_2028.csv"
    update_total_events(input_file, output_file) 