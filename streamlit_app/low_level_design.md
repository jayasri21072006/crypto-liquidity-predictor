# 🔧 Low-Level Design (LLD) Document

## Module Breakdown

### 1. Data Loading
- Load the CSV file using pandas.
- Parse datetime column.
- Drop missing/null values.

### 2. Feature Engineering
- Rolling mean for moving averages.
- Volatility using standard deviation.
- Liquidity ratio = 24h_volume / market cap.

### 3. Preprocessing
- Normalize skewed data (log1p transformations).
- Select numerical features for modeling.

### 4. Model Training
- Train/Test split: 80/20
- Model: Random Forest Regressor
- Evaluation: MAE, RMSE, R² Score

### 5. Deployment Interface
- Streamlit web UI with input sliders for features.
- Display predicted liquidity.
