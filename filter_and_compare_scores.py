import os
import pandas as pd

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

def filter_and_compare_scores(file1, file2, output_file):
    # 读取数据
    data1 = pd.read_csv(file1, encoding='utf-8-sig')
    data2 = pd.read_csv(file2, encoding='utf-8-sig')

    # 将国家名称转换为NOC
    data2['NOC'] = data2['NOC'].map(country_to_noc)

    # 合并数据，保留匹配的NOC
    merged_data = pd.merge(data1, data2, on='NOC', suffixes=('_file1', '_file2'))

    # 计算得分差异
    merged_data['difference'] = merged_data['score_file1'] - merged_data['score_file2']

    # 选择需要的列
    result = merged_data[['NOC', 'difference']]

    # 保存结果
    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"得分差异已保存到: {output_file}")

if __name__ == "__main__":
    file1 = r"D:/桌面/2025美国数学建模/结果/得分/medal_scores.csv"
    file2 = r"D:/桌面/2025美国数学建模/结果/得分/medal_scores_2024.csv"
    output_file = r"D:/桌面/2025美国数学建模/结果/得分/filtered_score_differences.csv"
    filter_and_compare_scores(file1, file2, output_file) 