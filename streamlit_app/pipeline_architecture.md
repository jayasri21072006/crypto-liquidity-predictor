# 🔁 Pipeline Architecture

### Step-by-Step Flow

1. **Data Ingestion**
   - Source: coin_gecko_2022-03-17.csv
   - Format: CSV → DataFrame

2. **Data Cleaning**
   - Drop NA rows
   - Datetime parsing

3. **Feature Engineering**
   - Moving averages (price, volume)
   - Volatility across 1h, 24h, 7d
   - Liquidity ratio (volume / market cap)

4. **Feature Selection**
   - Select relevant features for prediction

5. **Model Building**
   - Train Random Forest model
   - Save model as `.pkl`

6. **Deployment (Streamlit)**
   - Load `.pkl` model
   - Collect user inputs
   - Display prediction result
