import os
import pandas as pd

def average_predictions(input_file, output_file):
    # 读取数据
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # 检查是否包含必要的列
    required_columns = ['NOC', 'Gold', 'Silver', 'Bronze', 'Total']
    if not all(col in data.columns for col in required_columns):
        print("数据中缺少必要的列，无法处理。")
        return

    # 按 NOC 分组并计算平均值
    averaged_data = data.groupby('NOC', as_index=False).agg({
        'Gold': 'mean',
        'Silver': 'mean',
        'Bronze': 'mean',
        'Total': 'mean'
    })

    # 四舍五入
    averaged_data = averaged_data.round({
        'Gold': 0,
        'Silver': 0,
        'Bronze': 0,
        'Total': 0
    })

    # 按 Gold 降序排序并保存
    sorted_by_gold = averaged_data.sort_values(by='Gold', ascending=False)
    gold_output_file = os.path.join(os.path.dirname(output_file), 'averaged_predictions_by_gold.csv')
    sorted_by_gold.to_csv(gold_output_file, index=False, encoding='utf-8-sig')
    print(f"按 Gold 排序的平均值已保存到: {gold_output_file}")

    # 按 Total 降序排序并保存
    sorted_by_total = averaged_data.sort_values(by='Total', ascending=False)
    total_output_file = os.path.join(os.path.dirname(output_file), 'averaged_predictions_by_total.csv')
    sorted_by_total.to_csv(total_output_file, index=False, encoding='utf-8-sig')
    print(f"按 Total 排序的平均值已保存到: {total_output_file}")

if __name__ == "__main__":
    input_file = r"D:\桌面\2025美国数学建模\结果\predictions_2028.csv"
    output_file = r"D:\桌面\2025美国数学建模\结果\averaged_predictions_2028.csv"
    average_predictions(input_file, output_file)
