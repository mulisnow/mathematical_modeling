import pandas as pd
import os

# 主办国数据
host_data = {
    1896: 'GRE',
    1900: 'FRA',
    1904: 'USA',
    1908: 'GBR',
    1912: 'SWE',
    1916: None,  # Cancelled
    1920: 'BEL',
    1924: 'FRA',
    1928: 'NED',
    1932: 'USA',
    1936: 'GER',
    1940: None,  # Cancelled
    1944: None,  # Cancelled
    1948: 'GBR',
    1952: 'FIN',
    1956: 'AUS',
    1960: 'ITA',
    1964: 'JPN',
    1968: 'MEX',
    1972: 'GER',
    1976: 'CAN',
    1980: 'SOV',  # Soviet Union
    1984: 'USA',
    1988: 'KOR',
    1992: 'ESP',
    1996: 'USA',
    2000: 'AUS',
    2004: 'GRE',
    2008: 'CHN',
    2012: 'GBR',
    2016: 'BRA',
    2020: 'JPN',  # Postponed to 2021
    2024: 'FRA',
    2028: 'USA',
    2032: 'AUS'
}

# 数据文件所在目录
data_dir = "D:/桌面/2025美国数学建模/数据/特征工程"

# 遍历目录下的所有CSV文件
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]

# 检查是否找到CSV文件
if not data_files:
    print("未找到CSV文件，请检查数据目录路径。")
else:
    # 遍历每个数据文件
    for file in data_files:
        df = pd.read_csv(file)

        # 检查是否包含 Year 列
        if 'Year' not in df.columns:
            print(f"错误：文件 {file} 中未找到 'Year' 列")
            continue

        # 添加 Host 列
        df['Host'] = df.apply(lambda row: 1 if host_data.get(row['Year']) == row['NOC'] else 0, axis=1)

        # 保存更新后的数据
        df.to_csv(file, index=False, encoding='utf-8')  # 可以选择覆盖原文件或另存为新文件

    print("Host 列已成功添加到所有数据文件。")

# 这里可以添加与主办国相关的功能
# 示例：获取主办国信息
def get_host_info(year):
    # 这里可以根据年份返回主办国的信息
    host_data = {
        2024: 'France',
        2028: 'USA',
        # 添加更多年份和主办国
    }
    return host_data.get(year, 'Unknown')
