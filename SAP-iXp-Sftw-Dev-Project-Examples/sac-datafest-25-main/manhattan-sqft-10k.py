import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Leases.csv")

filtered_df = df[(df['market'] == 'Manhattan') & (df['leasedSF'] > 10000)]

plt.figure(figsize=(10, 6))
plt.hist(filtered_df['leasedSF'], bins=50, color='skyblue', edgecolor='black')
plt.title("Distribution of Manhattan Leases Over 10,000 sq ft", fontsize=14)
plt.xlabel("Square Footage (leasedSF)")
plt.ylabel("Number of Leases")
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.show()
