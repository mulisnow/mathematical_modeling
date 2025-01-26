import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os

# 1. Data Loading
def load_data(folder_path):
    all_files = os.listdir(folder_path)
    df_list = []
    for file in all_files:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

# Data path
folder_path = r"D:\桌面\2025美国数学建模\数据\名帅效应\Sport_NOC_coach"
df = load_data(folder_path)

# 2. Data Preparation
df = df.sort_values(by=["NOC", "Sport", "Year"])

# 3. Create Lag Variables
def create_lag_variables(df, lags):
    for lag in lags:
        df[f"coach_lag{lag}"] = df.groupby(["NOC", "Sport"])["coach"].shift(lag)
    return df

# Create lag variables for 1-5 years
df = create_lag_variables(df, lags=[1, 2, 3, 4, 5])

# Remove missing values (due to lag variables)
df = df.dropna()

# 4. Handle Categorical Variables
df = pd.get_dummies(df, columns=["NOC", "Sport"], drop_first=True)

# 5. Force Data Type Conversion
# Ensure all variables used for regression are numeric
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert boolean columns to integers
df = df.astype({col: 'int' for col in df.select_dtypes(include='bool').columns})

# Remove missing values again (due to forced conversion)
df = df.dropna()

# 6. Check Data Types
print("Data columns and their types:")
print(df.dtypes)

# 7. Model Building
def build_model(df, dependent_var, independent_vars):
    X = df[independent_vars]
    X = sm.add_constant(X)  # Add intercept
    y = df[dependent_var]

    # Check data types of X and y
    print("Data types of X:")
    print(X.dtypes)
    print("Data type of y:")
    print(y.dtype)

    # Check for NaN values in X and y
    print("Any NaN in X:", X.isnull().any().any())
    print("Any NaN in y:", y.isnull().any())

    model = sm.OLS(y, X).fit()
    return model

# Control Variables
control_vars = ["athletes_number", "Year"] + [col for col in df.columns if col.startswith("NOC_") or col.startswith("Sport_")]

# (1) Short-term Impact Model
short_term_vars = ["coach_lag1", "coach_lag2"] + control_vars
short_term_model = build_model(df, dependent_var="score", independent_vars=short_term_vars)

# (2) Long-term Impact Model
long_term_vars = ["coach_lag3", "coach_lag4", "coach_lag5"] + control_vars
long_term_model = build_model(df, dependent_var="score", independent_vars=long_term_vars)

# 8. Results Analysis
def print_model_results(model, model_name):
    print(f"===== {model_name} =====")
    print(model.summary())
    print("\n")

# Print short-term and long-term model results
print_model_results(short_term_model, "Short-term Impact Model")
print_model_results(long_term_model, "Long-term Impact Model")

# 9. Calculate Short-term and Long-term Impact
def calculate_effect(model, vars):
    coefficients = model.params
    effect = sum(coefficients[var] for var in vars)
    return effect

# Short-term impact
short_term_effect = calculate_effect(short_term_model, ["coach_lag1", "coach_lag2"])
print(f"Short-term impact (1-2 years): {short_term_effect:.2f} points")

# Long-term impact
long_term_effect = calculate_effect(long_term_model, ["coach_lag3", "coach_lag4", "coach_lag5"])
print(f"Long-term impact (3-5 years): {long_term_effect:.2f} points")

# 10. Visualization Results
def plot_effect_trend(short_term_model, long_term_model):
    years = [1, 2, 3, 4, 5]
    
    # Short-term effects
    short_term_effects = [
        short_term_model.params["coach_lag1"],
        short_term_model.params["coach_lag2"],
    ]
    
    # Long-term effects
    long_term_effects = [
        long_term_model.params["coach_lag3"],
        long_term_model.params["coach_lag4"],
        long_term_model.params["coach_lag5"],
    ]

    # Combine short-term and long-term effects
    all_effects = short_term_effects + long_term_effects
    all_years = years[:2] + years[2:]

    plt.figure(figsize=(10, 6))
    
    # Plot all effects with different markers
    plt.plot(all_years, all_effects, marker="o", linestyle="-", color="blue", label="Overall Coach Effect")
    
    # Highlight short-term and long-term segments with distinct colors
    plt.plot(years[:2], short_term_effects, marker="o", linestyle="--", color="orange", label="Short-term Effect")
    plt.plot(years[2:], long_term_effects, marker="o", linestyle="--", color="green", label="Long-term Effect")
    
    plt.axhline(y=0, color="red", linestyle="--", label="No Effect")
    plt.xlabel("Lag Years")
    plt.ylabel("Score Change")
    plt.title("Short-term and Long-term Coach Effect")
    plt.legend()
    plt.grid(True)

    # Save the plot to the specified directory
    output_dir = r"D:\桌面\2025美国数学建模\图像\第二问_名帅效应"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    plt.savefig(os.path.join(output_dir, "coach_effect_trend.png"), bbox_inches='tight', dpi=300)  # Save with high resolution
    plt.show()

# Draw the trend chart
plot_effect_trend(short_term_model, long_term_model)

# Results saving path
output_results_dir = r"D:\桌面\2025美国数学建模\结果\第二问"
os.makedirs(output_results_dir, exist_ok=True)  # Ensure the output directory exists

# 1. Save short-term model parameters
short_term_summary = short_term_model.summary2().tables[1]  # Get short-term model parameters summary
short_term_summary.to_csv(os.path.join(output_results_dir, "short_term_model_parameters.csv"), encoding='utf-8-sig')

# 2. Save long-term model parameters
long_term_summary = long_term_model.summary2().tables[1]  # Get long-term model parameters summary
long_term_summary.to_csv(os.path.join(output_results_dir, "long_term_model_parameters.csv"), encoding='utf-8-sig')

# 3. Save model performance metrics
performance_metrics = {
    "Short-term Model": {
        "R-squared": short_term_model.rsquared,
        "Adj. R-squared": short_term_model.rsquared_adj,
        "F-statistic": short_term_model.fvalue,
        "Prob (F-statistic)": short_term_model.f_pvalue,
        "AIC": short_term_model.aic,
        "BIC": short_term_model.bic,
    },
    "Long-term Model": {
        "R-squared": long_term_model.rsquared,
        "Adj. R-squared": long_term_model.rsquared_adj,
        "F-statistic": long_term_model.fvalue,
        "Prob (F-statistic)": long_term_model.f_pvalue,
        "AIC": long_term_model.aic,
        "BIC": long_term_model.bic,
    }
}

# Save performance metrics to a CSV file
performance_df = pd.DataFrame(performance_metrics).T
performance_df.to_csv(os.path.join(output_results_dir, "model_performance_metrics.csv"), encoding='utf-8-sig')

# 4. Detailed comments
with open(os.path.join(output_results_dir, "model_parameter_comments.txt"), "w", encoding='utf-8') as f:
    f.write("Short-term Model Parameters:\n")
    for param in short_term_summary.index:
        f.write(f"{param}: {short_term_summary.loc[param, 'Coef.']} (Coefficient for {param})\n")
    f.write("\n")
    
    f.write("Long-term Model Parameters:\n")
    for param in long_term_summary.index:
        f.write(f"{param}: {long_term_summary.loc[param, 'Coef.']} (Coefficient for {param})\n")
    f.write("\n")
    
    f.write("Performance Metrics:\n")
    for metric, value in performance_metrics["Short-term Model"].items():
        f.write(f"Short-term {metric}: {value}\n")
    for metric, value in performance_metrics["Long-term Model"].items():
        f.write(f"Long-term {metric}: {value}\n")

print("Model parameters and performance metrics saved successfully.")
