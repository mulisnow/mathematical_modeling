import pandas as pd

# 1. 读取数据
file_path = r"D:\桌面\2025美国数学建模\数据\名帅效应\国家项目历史奖牌\GBR_medal_summary.csv"
df = pd.read_csv(file_path)

# 2. 确定最近三届的年份
recent_years = [2024, 2020, 2016]  # 最近三届的年份
print("最近三届的年份：", recent_years)

# 3. 筛选近三届数据
recent_data = df[df['Year'].isin(recent_years)]

# 4. 计算历史平均奖牌数
historical_avg = df.groupby('Sport')['total_number'].mean().reset_index()
historical_avg.rename(columns={'total_number': 'historical_avg_total'}, inplace=True)

# 5. 计算近三届平均奖牌数
recent_avg = recent_data.groupby('Sport')['total_number'].mean().reset_index()
recent_avg.rename(columns={'total_number': 'recent_avg_total'}, inplace=True)

# 6. 合并历史数据和近三届数据
merged_data = pd.merge(historical_avg, recent_avg, on='Sport', how='inner')

# 7. 筛选历史上竞争力强但近三届表现较差的项目
# 定义历史竞争力强的标准：历史平均奖牌数 > 2
# 定义近三届表现较差的标准：近三届平均奖牌数 < 1
strong_historical = merged_data[merged_data['historical_avg_total'] > 3]
weak_recent = strong_historical[strong_historical['recent_avg_total'] < 2]

# 8. 输出结果
print("历史上竞争力强但近三届表现较差的项目：")
print(weak_recent)
