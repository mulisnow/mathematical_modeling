import pandas as pd

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
