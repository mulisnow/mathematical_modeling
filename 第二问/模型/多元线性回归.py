import pandas as pd
import statsmodels.api as sm
import os

# Define the directory path
data_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\Sport_NOC_coach"
output_corr_dir = r"D:\桌面\2025美国数学建模\数据\名帅效应\相关系数"

# Ensure the output directory exists
os.makedirs(output_corr_dir, exist_ok=True)

# Initialize lists to store results
correlations = []
regression_results = []

# Iterate over each CSV file in the data directory
for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the required columns exist
        required_columns = ['Year', 'Sport', 'athletes_number', 'coach', 'gold_number', 'silver_number', 'bronze_number', 'total_number', 'score']
        if not all(column in df.columns for column in required_columns):
            print(f"Skipping {filename}: Missing required columns")
            continue
        
        # Prepare the data for regression
        X1 = df[['Year', 'Sport', 'athletes_number', 'coach']]
        X1 = pd.get_dummies(X1, columns=['Sport'], drop_first=True)  # Convert categorical variable to dummy/indicator variables
        X1 = sm.add_constant(X1)  # Add a constant term for the intercept
        
        # Perform separate regressions for each medal count
        for medal in ['gold_number', 'silver_number', 'bronze_number', 'total_number']:
            y = df[medal]
            model = sm.OLS(y, X1).fit()
            regression_results.append((filename, medal, model.summary()))
        
        # Second regression: Predicting score
        y2 = df['score']
        model2 = sm.OLS(y2, X1).fit()
        regression_results.append((filename, 'Score', model2.summary()))
        
        # Calculate correlation coefficients
        corr_data = df[['Year', 'athletes_number', 'coach', 'gold_number', 'silver_number', 'bronze_number', 'total_number', 'score']]
        corr_matrix = corr_data.corr()
        
        # Save the correlation coefficients for the current country
        corr_file_path = os.path.join(output_corr_dir, f"{filename.split('.')[0]}_correlation.csv")
        corr_matrix.to_csv(corr_file_path, encoding='utf-8-sig')
        print(f"Correlation matrix saved to {corr_file_path}")

# Print the results
for filename, target, summary in regression_results:
    print(f"Regression results for {filename} - {target}:\n{summary}\n")
