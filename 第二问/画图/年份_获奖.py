import pandas as pd
import matplotlib.pyplot as plt
import os

# Set the font to SimHei to support Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is displayed correctly

# Define the directory paths
data_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\三个国家"
output_dir = r"D:\桌面\2025美国数学建模\图像\三个国家_第二问"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the years to highlight for each (NOC, Sport) pair
highlight_years = {
    ('KOR', 'Badminton'): 1999,
    ('USA', 'Volleyball'): 2005,
    ('CHN', 'Gymnastics'): 2021,
    ('USA', 'Athletics'): 1998,
    ('USA', 'Gymnastics'): 1998,
    ('JPN', 'Table Tennis'): 2008,
    ('CHN', 'Archery'): 2024,
    ('USA','Gymnastics'):1990,
    ('GBR','Tennis'):2012


}

# Iterate over each CSV file in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the required columns exist
        required_columns = ['Year', 'gold_number', 'silver_number', 'bronze_number', 'total_number', 'score']
        if not all(column in df.columns for column in required_columns):
            print(f"Skipping {filename}: Missing required columns")
            continue
        
        # Extract NOC and Sport from the filename
        parts = filename.split('_')
        sport = parts[0]
        noc = parts[1]
        
        # Plot the medal data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Year'], df['gold_number'], label='Gold', marker='o', color='gold')
        plt.plot(df['Year'], df['silver_number'], label='Silver', marker='o', color='silver')
        plt.plot(df['Year'], df['bronze_number'], label='Bronze', marker='o', color='brown')
        plt.plot(df['Year'], df['total_number'], label='Total', marker='o', color='blue')
        
        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Number of Medals')
        plt.title(f"Medal Counts Over Years - {filename.split('.')[0]}")
        plt.legend()
        plt.grid(True)
        
        # Highlight the specific year if applicable
        if (noc, sport) in highlight_years:
            highlight_year = highlight_years[(noc, sport)]
            plt.axvline(x=highlight_year, color='red', linestyle='--', label=f'Highlight {highlight_year}')
            plt.text(highlight_year, plt.ylim()[1] * 0.9, f'{highlight_year}', color='red', ha='center')
        
        # Save the medal plot
        output_file_path = os.path.join(output_dir, f"{filename.split('.')[0]}_medal_plot.png")
        plt.savefig(output_file_path)
        plt.close()
        
        print(f"Medal plot saved to {output_file_path}")
        
        # Plot the score data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Year'], df['score'], label='Score', marker='o', color='purple')
        
        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('Score')
        plt.title(f"Score Over Years - {filename.split('.')[0]}")
        plt.legend()
        plt.grid(True)
        
        # Highlight the specific year if applicable
        if (noc, sport) in highlight_years:
            highlight_year = highlight_years[(noc, sport)]
            plt.axvline(x=highlight_year, color='red', linestyle='--', label=f'Highlight {highlight_year}')
            plt.text(highlight_year, plt.ylim()[1] * 0.9, f'{highlight_year}', color='red', ha='center')
        
        # Save the score plot
        output_file_path = os.path.join(output_dir, f"{filename.split('.')[0]}_score_plot.png")
        plt.savefig(output_file_path)
        plt.close()
        
        print(f"Score plot saved to {output_file_path}")
