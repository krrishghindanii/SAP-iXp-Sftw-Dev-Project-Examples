import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("Leases.csv")
print("🔍 Available columns in Leases.csv:")
print(df.columns.tolist())

rent_candidates = [col for col in df.columns if 'rent' in col.lower()]
if not rent_candidates:
    raise ValueError("No rent-related column found.")
rent_col = rent_candidates[0]
print(f"✅ Using '{rent_col}' as rent column.\n")

if 'year' not in df.columns or 'quarter' not in df.columns:
    raise ValueError("'year' or 'quarter' column missing from CSV.")

df = df.dropna(subset=[rent_col, 'year', 'quarter'])

quarter_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
df['date'] = df.apply(lambda row: pd.to_datetime(f"{int(row['year'])}-{quarter_map[row['quarter']]}-01"), axis=1)

ts = df.groupby('date')[rent_col].mean().sort_index()

print("📈 Fitting ARIMA model...")
model = ARIMA(ts, order=(1, 1, 1))  # (p,d,q) can be tuned
model_fit = model.fit()

forecast_steps = 4
forecast = model_fit.forecast(steps=forecast_steps)
forecast.index = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=3), periods=forecast_steps, freq='QS')

plt.figure(figsize=(12, 6))
plt.plot(ts, label='Historical Rent', marker='o')
plt.plot(forecast, label='Forecast (2025)', marker='o', linestyle='--', color='orange')
plt.title("ARIMA Forecast – Average Rent per Quarter", fontsize=16, weight='bold')
plt.xlabel("Date")
plt.ylabel("Average Rent")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("forecast_rent_2025.png", dpi=300)
plt.show()

print("\n📊 Forecasted Rent for 2025:")
print(forecast.round(2))
