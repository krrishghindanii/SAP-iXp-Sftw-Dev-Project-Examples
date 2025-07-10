import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

df = pd.read_csv("Leases.csv")
markets = ['Tampa', 'Seattle', 'South Florida', 'Atlanta', 'Austin', 'Baltimore']

df = df[df['market'].isin(markets)]
df = df.dropna(subset=['availability_proportion', 'year', 'quarter'])

q_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
df['date'] = df.apply(lambda row: pd.to_datetime(f"{int(row['year'])}-{q_map[row['quarter']]}-01"), axis=1)

grouped = df.groupby(['market', 'date'])['availability_proportion'].mean().reset_index()
pivot_df = grouped.pivot(index='date', columns='market', values='availability_proportion').sort_index()

for market in markets:
    print(f"\n📈 Forecast for {market}:")
    ts = pivot_df[market].dropna()

    if len(ts) < 8:
        print("  Not enough data for ARIMA.")
        continue

    model = ARIMA(ts, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast next 4 quarters (2025)
    forecast = model_fit.forecast(steps=2)
    forecast.index = pd.date_range(start=ts.index[-1] + pd.DateOffset(months=3), periods=2, freq='QS')

    # Print forecast
    print(forecast.round(4))

    y_max = max(ts.max(), forecast.max()) + 0.01  # small buffer

    plt.figure(figsize=(10, 5))
    plt.plot(ts, label='Historical', marker='o')
    plt.plot(forecast, label='Forecast (2025)', linestyle='--', marker='o', color='orange')
    plt.title(f"{market} – Availability Rate Forecast (ARIMA)")
    plt.ylabel("Availability Proportion")
    plt.xlabel("Date")
    plt.ylim(0, 0.3)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
