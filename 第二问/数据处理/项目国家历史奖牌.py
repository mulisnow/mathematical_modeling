import pandas as pd

# Define the file paths
input_file_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"

# Define the NOCs to process
nocs_to_process = ["USA", "IND", "GBR"]

# Read the CSV file
df = pd.read_csv(input_file_path)

# Initialize a summary DataFrame to store results for each NOC
summary_results = {}

# Process each NOC
for noc in nocs_to_process:
    # Filter the DataFrame for the specific NOC
    filtered_df = df[df['NOC'] == noc]

    # Group by NOC, Sport, and Year to calculate medal counts
    medal_summary_df = filtered_df.groupby(['NOC', 'Sport', 'Year']).agg(
        gold_number=('Medal', lambda x: (x == 'Gold').sum()),
        silver_number=('Medal', lambda x: (x == 'Silver').sum()),
        bronze_number=('Medal', lambda x: (x == 'Bronze').sum())
    ).reset_index()

    # Calculate total number of medals
    medal_summary_df['total_number'] = medal_summary_df['gold_number'] + medal_summary_df['silver_number'] + \
                                       medal_summary_df['bronze_number']

    # Calculate the number of athletes per year
    athletes_summary_df = filtered_df.groupby(['NOC', 'Sport', 'Year']).agg(
        athletes_number=('Name', 'count')  # Assuming 'Name' is a unique identifier for athletes
    ).reset_index()

    # Merge the medal summary and athletes summary
    summary_df = pd.merge(medal_summary_df, athletes_summary_df, on=['NOC', 'Sport', 'Year'])

    # Calculate the score
    summary_df['score'] = summary_df['gold_number'] * 10 + summary_df['silver_number'] * 8 + summary_df['bronze_number'] * 7

    # Sort the summary DataFrame by Year in descending order
    summary_df = summary_df.sort_values(by='Year', ascending=False)

    # Store the results in the summary_results dictionary
    summary_results[noc] = summary_df

    # Define the output file path based on the NOC
    output_file_path = f"D:\\桌面\\2025美国数学建模\\数据\\名帅效应\\国家项目历史奖牌\\{noc}_medal_summary.csv"

    # Save the summarized DataFrame to a new CSV file
    summary_df.to_csv(output_file_path, index=False)

    print(f"Summarized data for {noc} saved to {output_file_path}")

