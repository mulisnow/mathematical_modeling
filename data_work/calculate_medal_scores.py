import os
import pandas as pd

def calculate_medal_scores(input_file, output_dir):
    # 读取数据
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # 检查是否包含必要的列
    required_columns = ['NOC', 'Gold', 'Silver', 'Bronze']
    if not all(col in data.columns for col in required_columns):
        print("数据中缺少必要的列，无法处理。")
        return

    # 计算每个国家的奖牌得分
    data['score'] = data['Gold'] * 10 + data['Silver'] * 8 + data['Bronze'] * 7

    # 按得分降序排序
    sorted_data = data[['NOC', 'score']].sort_values(by='score', ascending=False)

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 保存结果到指定路径
    output_file = os.path.join(output_dir, 'medal_scores_2024.csv')
    sorted_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"奖牌得分已保存到: {output_file}")

if __name__ == "__main__":
    input_file = r"D:/桌面/2025美国数学建模/结果/averaged_predictions_by_gold_2024.csv"
    output_dir = r"D:/桌面/2025美国数学建模/结果/得分"
    calculate_medal_scores(input_file, output_dir) 