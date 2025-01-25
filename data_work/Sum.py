import pandas as pd
import os

# 定义国家名称到简称的映射
country_to_noc = {
    "United States": "USA",
    "China": "CHN",
    "Japan": "JPN",
    "Great Britain": "GBR",
    "ROC": "ROC",
    "Australia": "AUS",
    "Netherlands": "NED",
    "France": "FRA",
    "Germany": "GER",
    "Italy": "ITA",
    "Canada": "CAN",
    "Brazil": "BRA",
    "New Zealand": "NZL",
    "Cuba": "CUB",
    "Hungary": "HUN",
    "South Korea": "KOR",
    "Poland": "POL",
    "Czech Republic": "CZE",
    "Kenya": "KEN",
    "Norway": "NOR",
    "Jamaica": "JAM",
    "Spain": "ESP",
    "Sweden": "SWE",
    "Switzerland": "SUI",
    "Denmark": "DEN",
    "Croatia": "CRO",
    "Iran": "IRI",
    "Serbia": "SRB",
    "Belgium": "BEL",
    "Bulgaria": "BUL",
    "Slovenia": "SLO",
    "Uzbekistan": "UZB",
    "Georgia": "GEO",
    "Chinese Taipei": "TPE",
    "Turkey": "TUR",
    "Greece": "GRE",
    "Uganda": "UGA",
    "Ecuador": "ECU",
    "Ireland": "IRL",
    "Israel": "ISR",
    "Qatar": "QAT",
    "Bahamas": "BAH",
    "Kosovo": "KOS",
    "Ukraine": "UKR",
    "Belarus": "BLR",
    "Romania": "ROU",
    "Venezuela": "VEN",
    "India": "IND",
    "Hong Kong": "HKG",
    "Philippines": "PHI",
    "Slovakia": "SVK",
    "South Africa": "RSA",
    "Austria": "AUT",
    "Egypt": "EGY",
    "Indonesia": "INA",
    "Ethiopia": "ETH",
    "Portugal": "POR",
    "Tunisia": "TUN",
    "Estonia": "EST",
    "Fiji": "FIJ",
    "Latvia": "LAT",
    "Thailand": "THA",
    "Bermuda": "BER",
    "Morocco": "MAR",
    "Puerto Rico": "PUR",
    "Colombia": "COL",
    "Azerbaijan": "AZE",
    "Dominican Republic": "DOM",
    "Armenia": "ARM",
    "Kyrgyzstan": "KGZ",
    "Mongolia": "MGL",
    "Argentina": "ARG",
    "San Marino": "SMR",
    "Jordan": "JOR",
    "Malaysia": "MAS",
    "Nigeria": "NGR",
    "Bahrain": "BRN",
    "Lithuania": "LTU",
    "Namibia": "NAM",
    "North Macedonia": "MKD",
    "Saudi Arabia": "KSA",
    "Turkmenistan": "TKM",
    "Kazakhstan": "KAZ",
    "Mexico": "MEX",
    "Finland": "FIN",
    "Botswana": "BOT",
    "Burkina Faso": "BUR",
    "Ghana": "GHA",
    "Grenada": "GRN",
    "Ivory Coast": "CIV",
    "Kuwait": "KUW",
    "Moldova": "MDA",
    "Syria": "SYR"
}

# 读取奖牌数据
medal_file = r"D:\桌面\2025美国数学建模\题目\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_medal_counts.csv"

# 检查奖牌文件是否存在
if not os.path.exists(medal_file):
    print(f"奖牌数据文件未找到: {medal_file}")
else:
    print(f"成功找到奖牌数据文件: {medal_file}")

# 读取奖牌数据
try:
    medal_data = pd.read_csv(medal_file)
    print("奖牌数据读取成功")
    print(medal_data.head())  # 查看前几行数据
except Exception as e:
    print(f"读取奖牌数据时出错: {e}")

# 替换NOC国家名称为简称
medal_data["NOC"] = medal_data["NOC"].map(country_to_noc)

feature_folder = "D:/桌面/2025美国数学建模/数据/特征工程"

# 检查特征工程目录是否存在
if not os.path.exists(feature_folder):
    print(f"特征工程目录未找到: {feature_folder}")
else:
    print(f"成功找到特征工程目录: {feature_folder}")

# 遍历特征工程文件夹
for filename in os.listdir(feature_folder):
    print(f"检测到文件: {filename}")
    if filename.startswith("feature_analysis_") and filename.endswith(".csv"):

        file_path = os.path.join(feature_folder, filename)
        print(f"正在处理文件: {file_path}")

        # 读取特征工程数据
        try:
            feature_data = pd.read_csv(file_path)
            print(f"成功读取文件: {filename}")
            print("文件列名:", feature_data.columns.tolist())  # 输出列名

            # 检查是否存在Year和NOC列
            if "Year" not in feature_data.columns or "NOC" not in feature_data.columns:
                print(f"文件 {file_path} 缺少 'Year' 或 'NOC' 列，未处理。")
                continue

            # 执行合并
            merged_data = feature_data.merge(
                medal_data[["Year", "NOC", "Gold", "Silver", "Bronze", "Total"]],
                how="left",
                on=["Year", "NOC"]
            )

            # 填充缺失的奖牌数据为空值的列为0
            merged_data["Gold"].fillna(0, inplace=True)
            merged_data["Silver"].fillna(0, inplace=True)
            merged_data["Bronze"].fillna(0, inplace=True)
            merged_data["Total"].fillna(0, inplace=True)

            # 检查合并后的数据
            print("合并后数据示例:", merged_data.head())

            # 保存更新后的数据
            merged_data.to_csv(file_path, index=False)
            print(f"已成功更新文件: {file_path}")

        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
