import os
import pandas as pd

def consolidate_events(input_dir, output_dir, events):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 创建一个字典来存储每个事件的结果
    consolidated_data = {event: [] for event in events}

    # 遍历输入目录中的每个文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_dir, filename)
            print(f"正在处理文件: {file_path}")
            data = pd.read_csv(file_path, encoding='utf-8-sig')

            # 检查是否包含必要的列
            if 'Event' not in data.columns or 'NOC' not in data.columns or 'importance_score' not in data.columns:
                print(f"文件 {file_path} 缺少必要的列，跳过该文件。")
                continue

            # 筛选包含指定事件的行
            for event in events:
                filtered_data = data[data['Event'].str.contains(event, case=False, na=False)]
                if not filtered_data.empty:
                    consolidated_data[event].append(filtered_data[['NOC', 'Event', 'importance_score']])

    # 保存整合后的数据
    for event, frames in consolidated_data.items():
        if frames:
            combined_data = pd.concat(frames, ignore_index=True)
            output_file_path = os.path.join(output_dir, f"{event.lower()}_consolidated.csv")
            combined_data.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            print(f"{event} 的整合结果已保存到: {output_file_path}")
        else:
            print(f"没有找到 {event} 的相关数据。")

if __name__ == "__main__":
    input_directory = r"D:\桌面\2025美国数学建模\数据\预测"  # 输入目录
    output_directory = r"D:\桌面\2025美国数学建模\数据\整合结果"  # 输出目录
    events_to_consolidate = ['Baseball', 'Lacrosse', 'Cricket']  # 要整合的事件
    consolidate_events(input_directory, output_directory, events_to_consolidate) 