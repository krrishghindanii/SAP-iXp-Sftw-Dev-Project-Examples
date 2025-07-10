import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("Leases.csv")

df = df[df['market'] == 'Manhattan']

df = df.dropna(subset=['availability_proportion', 'year', 'quarter'])

q_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
df['date'] = df.apply(lambda row: pd.to_datetime(f"{int(row['year'])}-{q_map[row['quarter']]}-01"), axis=1)

ts = df.groupby('date')['availability_proportion'].mean().sort_index()

model = ARIMA(ts, order=(1, 1, 1))
model_fit = model.fit()

forecast = model_fit.forecast(steps=4)
forecast.index = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=3), periods=4, freq='QS')

plt.figure(figsize=(10, 5))
plt.plot(ts, label='Historical', marker='o')
plt.plot(forecast, label='Forecast (2025)', linestyle='--', marker='o', color='orange')
plt.title("Manhattan Availability Rate Forecast (ARIMA)")
plt.ylabel("Availability Proportion")
plt.xlabel("Date")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print("\n📊 2025 Forecasted Availability Rates:")
print(forecast.round(4))
