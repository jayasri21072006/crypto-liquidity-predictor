# High-Level Design Document (HLD)

## 🎯 Objective
To predict the liquidity of cryptocurrencies using historical price and market data.

## 📦 System Architecture
1. **Data Ingestion** – Load & clean data
2. **Feature Engineering** – Moving averages, volatility, liquidity ratio
3. **Model Training** – RandomForestRegressor
4. **Evaluation** – MAE, RMSE, R²
5. **Deployment** – Streamlit for local testing

## 🛠 Components
- Data Pipeline
- ML Model Trainer
- Evaluation Module
- Streamlit Interface
