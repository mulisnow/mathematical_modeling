import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
import xgboost as xgb
import lightgbm as lgb
from tqdm import tqdm
from joblib import Parallel, delayed

# 数据文件所在目录
data_dir = "D:/桌面/2025美国数学建模/数据/特征工程"

# 遍历目录下的所有CSV文件
data_files = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith('.csv')]

# 检查是否找到CSV文件
if not data_files:
    print("未找到CSV文件，请检查数据目录路径。")
else:
    # 初始化一个 DataFrame 用于存储所有年份的数据
    all_data = pd.DataFrame()

    # 读取每个文件并合并数据
    for file in data_files:
        df = pd.read_csv(file)
        # 只使用2000年及以后的数据
        df = df[df['Year'].astype(int) >= 2000]
        all_data = pd.concat([all_data, df], ignore_index=True)

    # 处理缺失值
    all_data = all_data.fillna(0)

    # 检查数据是否为空
    if all_data.empty:
        print("数据为空，请检查数据文件内容。")
    else:
        # 提取特征和目标变量
        features = all_data[['NOC', 'Sport', 'Event', 'athletes_number', 'Total Events', 'Year',
                             'gold_number_previous', 'silver_number_previous', 'bronze_number_previous',
                             'total_number_previous', 'Host']].copy()
        targets = all_data[['gold_number', 'silver_number', 'bronze_number', 'total_number']].copy()

        # 对分类特征进行编码
        le_noc = LabelEncoder()
        le_sport = LabelEncoder()
        le_event = LabelEncoder()

        features['NOC'] = le_noc.fit_transform(features['NOC'])
        features['Sport'] = le_sport.fit_transform(features['Sport'])
        features['Event'] = le_event.fit_transform(features['Event'])

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

        # 定义模型列表
        models = {
            "Random Forest": RandomForestRegressor(random_state=42, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42),
            "Linear Regression": LinearRegression(),
            "Support Vector Regression": SVR(),
            "Decision Tree": DecisionTreeRegressor(random_state=42),
            "Polynomial Regression": make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
            "Neural Network": MLPRegressor(random_state=42, max_iter=1000),
            "XGBoost": xgb.XGBRegressor(random_state=42, n_jobs=-1),
            "LightGBM": lgb.LGBMRegressor(random_state=42, n_jobs=-1)
        }

        # 训练和评估每个模型
        def train_and_evaluate(model_name, model):
            print(f"\n{model_name} Results:")
            for col in targets.columns:
                # 训练模型
                model.fit(X_train, y_train[col])

                # 预测
                predictions = model.predict(X_test)

                # 计算评估指标
                mse = mean_squared_error(y_test[col], predictions)
                r2 = r2_score(y_test[col], predictions)
                print(f"{col}: MSE = {mse:.2f}, R² = {r2:.2f}")

        Parallel(n_jobs=-1)(delayed(train_and_evaluate)(model_name, model) for model_name, model in tqdm(models.items(), desc="Training Models"))

        # 预测 2028 年洛杉矶夏季奥运会的奖牌数
        # 这里可以根据模型的预测结果进行分析和输出
        # 例如，使用训练好的模型对未来数据进行预测