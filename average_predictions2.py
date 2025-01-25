import os
import pandas as pd

def average_predictions(input_file, output_file):
    # 读取数据
    data = pd.read_csv(input_file, encoding='utf-8-sig')

    # 检查是否包含必要的列
    required_columns = [
        'NOC', 'Predicted Gold Medals', 'Gold Lower Bound', 'Gold Upper Bound',
        'Predicted Silver Medals', 'Silver Lower Bound', 'Silver Upper Bound',
        'Predicted Bronze Medals', 'Bronze Lower Bound', 'Bronze Upper Bound',
        'Predicted Total Medals', 'Total Lower Bound', 'Total Upper Bound'
    ]
    if not all(col in data.columns for col in required_columns):
        print("数据中缺少必要的列，无法处理。")
        return

    # 按 NOC 分组并计算平均值
    averaged_data = data.groupby('NOC', as_index=False).agg({
        'Predicted Gold Medals': 'mean',
        'Gold Lower Bound': 'mean',
        'Gold Upper Bound': 'mean',
        'Predicted Silver Medals': 'mean',
        'Silver Lower Bound': 'mean',
        'Silver Upper Bound': 'mean',
        'Predicted Bronze Medals': 'mean',
        'Bronze Lower Bound': 'mean',
        'Bronze Upper Bound': 'mean',
        'Predicted Total Medals': 'mean',
        'Total Lower Bound': 'mean',
        'Total Upper Bound': 'mean'
    })

    # 四舍五入
    averaged_data = averaged_data.round({
        'Predicted Gold Medals': 0,
        'Gold Lower Bound': 0,
        'Gold Upper Bound': 0,
        'Predicted Silver Medals': 0,
        'Silver Lower Bound': 0,
        'Silver Upper Bound': 0,
        'Predicted Bronze Medals': 0,
        'Bronze Lower Bound': 0,
        'Bronze Upper Bound': 0,
        'Predicted Total Medals': 0,
        'Total Lower Bound': 0,
        'Total Upper Bound': 0
    })

    # 保存结果到指定路径
    averaged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"平均值已保存到: {output_file}")

if __name__ == "__main__":
    input_file = r"D:/桌面/2025美国数学建模/结果/预测区间/predictions_with_intervals.csv"
    output_file = r"D:/桌面/2025美国数学建模/结果/预测区间/averaged_predictions.csv"
    average_predictions(input_file, output_file) 