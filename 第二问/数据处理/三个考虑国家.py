import pandas as pd
import os

# Define the input directory and output directory
input_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\国家项目历史奖牌"
output_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\三个国家"
os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

# Define the NOCs and their corresponding sports
nocs_sports = {
    "JPN": ["Volleyball"],
    "USA": ["Golf", "Synchronized Swimming", "Sailing"],
    "GBR": ["Football", "Shooting", "Tennis"]
}

# Initialize a list to store the filtered DataFrames
filtered_dfs = []

# Iterate over each CSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the required columns exist
        if 'NOC' in df.columns and 'Sport' in df.columns:
            # Add coach column, set Year 2024 value to 1, others to 0
            df['coach'] = 0
            df.loc[df['Year'] == 2024, 'coach'] = 1
            
            # Filter the DataFrame based on NOC and Sport
            for noc, sports in nocs_sports.items():
                for sport in sports:
                    filtered_df = df[(df['NOC'] == noc) & (df['Sport'] == sport)]
                    
                    # If there are any results, save them
                    if not filtered_df.empty:
                        output_file_name = f"{noc}_{sport}.csv"
                        output_file_path = os.path.join(output_dir, output_file_name)
                        filtered_df.to_csv(output_file_path, index=False)
                        print(f"Filtered data for {noc} in {sport} saved to {output_file_path}")

print("Data filtering and saving completed.")
