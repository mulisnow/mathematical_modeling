import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_medals(input_dir, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历输入目录中的每个文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            country_data = pd.read_csv(os.path.join(input_dir, filename))

            # 提取国家名称
            country_name = os.path.splitext(filename)[0]

            # 计算总数
            country_data['Total'] = country_data['Gold'] + country_data['Silver'] + country_data['Bronze']

            # 绘制图像
            plt.figure(figsize=(12, 8))
            plt.plot(country_data['Year'], country_data['Gold'], marker='o', label='Gold', color='gold')
            plt.plot(country_data['Year'], country_data['Silver'], marker='o', label='Silver', color='silver')
            plt.plot(country_data['Year'], country_data['Bronze'], marker='o', label='Bronze', color='brown')
            plt.plot(country_data['Year'], country_data['Total'], marker='o', label='Total', color='blue')  # 添加总数的绘制

            plt.title(f'Medals Over Years for {country_name}')
            plt.xlabel('Year')
            plt.ylabel('Count')
            plt.xticks(country_data['Year'], rotation=45)  # 旋转年份标签以便更好地显示
            plt.legend()
            plt.grid()

            # 保存图像
            plt.savefig(os.path.join(output_dir, f'{country_name}_medals_over_years.png'))
            plt.close()

if __name__ == "__main__":
    input_dir = r"D:\桌面\2025美国数学建模\数据\国家历史奖牌"  # 输入目录
    output_dir = r"D:\桌面\2025美国数学建模\图像\国家历史奖牌"  # 输出目录
    plot_medals(input_dir, output_dir)
