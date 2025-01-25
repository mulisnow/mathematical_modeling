import os
import pandas as pd

def filter_events(input_dir, output_dir, events):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的每个文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            print(f"正在处理文件: {file_path}")
            data = pd.read_csv(file_path, encoding='utf-8-sig')

            # 检查是否包含必要的列
            if 'Event' not in data.columns or 'importance_score' not in data.columns:
                print(f"文件 {file_path} 缺少必要的列，跳过该文件。")
                continue

            # 从文件名中提取 NOC
            noc = filename.split('_')[0]  # 假设文件名格式为 "NOC_event_importance.csv"
            print(f"提取的 NOC: {noc}")

            # 筛选包含指定事件的行
            filtered_data = data[data['Event'].str.contains('|'.join(events), case=False, na=False)]
            print(f"筛选后的数据行数: {len(filtered_data)}")

            # 如果有符合条件的行，保存到新的文件
            if not filtered_data.empty:
                filtered_data['NOC'] = noc  # 添加 NOC 列
                output_file_path = os.path.join(output_dir, f"filtered_{filename}")
                filtered_data[['NOC', 'Event', 'importance_score']].to_csv(output_file_path, index=False, encoding='utf-8-sig')
                print(f"已保存筛选结果到: {output_file_path}")
            else:
                print(f"文件 {filename} 中没有找到符合条件的事件。")

if __name__ == "__main__":
    input_directory = r"D:\桌面\2025美国数学建模\数据\重要程度"
    output_directory = r"D:\桌面\2025美国数学建模\数据\预测"
    events_to_filter = ['Baseball', 'Lacrosse', 'Cricket']  # 要筛选的事件
    filter_events(input_directory, output_directory, events_to_filter) 