import pandas as pd

# Define the file paths
input_file_path = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv"

# Define a mapping of coaches to their respective NOCs and sports
coach_mapping = {
    '李矛': ('KOR', 'Badminton'),
    '郎平': ('USA', 'Volleyball'),
    'BLIZNYUK Anastasia': ('CHN', 'Gymnastics'),
    '李梨': ('USA', 'Athletics'),
    '乔良': ('USA', 'Gymnastics'),
    '中泽锐': ('JPN', 'Table Tennis'),
    '权容学': ('CHN', 'Archery'),
    'Béla Károlyi': ('USA', 'Gymnastics'),
    'Ivan Lendl': ('GBR', 'Tennis'),
}

# Define the years to set coach value
highlight_years = {
    ('KOR', 'Badminton'): 1999,
    ('USA', 'Volleyball'): 2005,
    ('CHN', 'Gymnastics'): 2021,
    ('USA', 'Athletics'): 1998,
    ('USA', 'Gymnastics'): 1998,
    ('JPN', 'Table Tennis'): 2008,
    ('CHN', 'Archery'): 2024,
    ('USA', 'Gymnastics'): 1990,
    ('GBR', 'Tennis'): 2012
}

# Read the CSV file
df = pd.read_csv(input_file_path)

# Process each coach
for coach, (noc, sport) in coach_mapping.items():
    # Filter the DataFrame for the specific Sport and NOC
    filtered_df = df[(df['Sport'] == sport) & (df['NOC'] == noc)]
    
    # Group by NOC, Sport, and Year to calculate medal counts
    medal_summary_df = filtered_df.groupby(['NOC', 'Sport', 'Year']).agg(
        gold_number=('Medal', lambda x: (x == 'Gold').sum()),
        silver_number=('Medal', lambda x: (x == 'Silver').sum()),
        bronze_number=('Medal', lambda x: (x == 'Bronze').sum())
    ).reset_index()
    
    # Calculate total number of medals
    medal_summary_df['total_number'] = medal_summary_df['gold_number'] + medal_summary_df['silver_number'] + medal_summary_df['bronze_number']
    
    # Calculate the number of athletes per year
    athletes_summary_df = filtered_df.groupby(['NOC', 'Sport', 'Year']).agg(
        athletes_number=('Name', 'count')  # Assuming 'Name' is a unique identifier for athletes
    ).reset_index()
    
    # Merge the medal summary and athletes summary
    summary_df = pd.merge(medal_summary_df, athletes_summary_df, on=['NOC', 'Sport', 'Year'])
    
    # Calculate the score
    summary_df['score'] = summary_df['gold_number'] * 10 + summary_df['silver_number'] * 8 + summary_df['bronze_number'] * 7
    
    # Add the coach column based on the year
    if (noc, sport) in highlight_years:
        year_threshold = highlight_years[(noc, sport)]
        summary_df['coach'] = summary_df['Year'].apply(lambda x: 1 if x > year_threshold else 0)
    
    # Sort the summary DataFrame by Year in descending order
    summary_df = summary_df.sort_values(by='Year', ascending=False)
    
    # Define the output file path based on the coach's name
    output_file_path = f"D:\\桌面\\2025美国数学建模\\数据\\名帅效应\\Sport_NOC_coach\\{sport}_{noc}_{coach}.csv"
    
    # Save the summarized DataFrame to a new CSV file
    summary_df.to_csv(output_file_path, index=False)
    
    print(f"Summarized data for {coach} saved to {output_file_path}")
