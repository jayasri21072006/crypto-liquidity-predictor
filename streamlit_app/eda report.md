🧪 Exploratory Data Analysis (EDA) Report
📂 1. Dataset Overview
Dataset Name: coin_gecko_2022-03-17.csv

Total Records: ~190+

Columns:

coin, symbol, price, 1h, 24h, 7d, 24h_volume, mkt_cap, date

🔍 2. Missing Values
All missing rows were dropped.

Dataset is now clean and ready for analysis.

📊 3. Summary Statistics:
price: Varies by coin. Distribution is uneven across coins depending on popularity and market share.

1h, 24h, 7d (%): These represent percentage changes in value over time. The data is highly skewed, with both negative and positive extremes indicating market volatility.

24h_volume: Exhibits high variance and is right-skewed. Some coins have trading volumes near zero, while others trade in millions.

mkt_cap: Very skewed. Market capitalization ranges from very small coins to billion-dollar assets. There's a wide spread in the data.

Note: Due to the skewness in volume and market cap features, log transformations (such as log1p()) were applied to normalize the distributions and improve model learning efficiency.

📈 4. Feature Distributions
Used histograms to plot all numerical columns.

Applied log transformation on 24h_volume, mkt_cap for normalization.

🔗 5. Correlation Analysis
Feature	Correlation with 24h_volume
price	Moderate
mkt_cap	Strong Positive
24h	Mild Negative
7d	Low correlation

Heatmap shows that mkt_cap and price are strong indicators of liquidity trends.

🎯 6. Insights
Cryptocurrencies with higher market caps tend to have better liquidity.

Volatility (standard deviation across 1h, 24h, 7d) is useful in explaining unstable liquidity.

Newly engineered features like ma_price, ma_volume, volatility, and liquidity_ratio boost model performance.

