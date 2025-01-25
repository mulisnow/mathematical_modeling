import os
import pandas as pd

def find_noc_with_all_zero_total_number(directory):
    # 用于存储每个 NOC 在所有文件中的 total_number 列值的列表
    noc_total_number_dict = {}

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            try:
                # 读取 CSV 文件
                df = pd.read_csv(file_path)

                # 检查是否包含 NOC 和 total_number 列
                if 'NOC' in df.columns and 'total_number' in df.columns:
                    # 遍历 DataFrame 的每一行
                    for index, row in df.iterrows():
                        noc = row['NOC']
                        total_number = row['total_number']

                        # 如果 NOC 不在字典中，初始化其 total_number 值列表
                        if noc not in noc_total_number_dict:
                            noc_total_number_dict[noc] = []

                        # 将 total_number 值添加到对应 NOC 的列表中
                        noc_total_number_dict[noc].append(total_number)
            except Exception as e:
                print(f"Error reading file {filename}: {e}")

    # 找出所有 total_number 列都为 0 的 NOC
    noc_with_all_zero_total_number = []
    for noc, total_numbers in noc_total_number_dict.items():
        if all(total_number == 0 for total_number in total_numbers):
            noc_with_all_zero_total_number.append(noc)

    return noc_with_all_zero_total_number

if __name__ == "__main__":
    input_directory = r"D:\桌面\2025美国数学建模\数据\特征工程"
    output_directory = r"D:\桌面\2025美国数学建模\数据\一次都没获奖"
    output_file = os.path.join(output_directory, "noc_with_all_zero_total_number.csv")

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    noc_list = find_noc_with_all_zero_total_number(input_directory)

    # 创建 DataFrame 并保存到文件
    df_output = pd.DataFrame({'NOC': noc_list})
    df_output.to_csv(output_file, index=False)

    print(f"所有数据文件里 total_number 列都为 0 的 NOC 已保存到 {output_file}")