import pandas as pd
import matplotlib.pyplot as plt
import json

filename = 'dlis100.json'

with open(filename, 'r') as file:
    data = json.load(file)

rows = []
for ratio, sub_dict in data.items():
    for int_value, (sat_status, steps) in sub_dict.items():
        rows.append({'ratio': float(ratio), 'int_value': int(int_value), 'sat_status': sat_status, 'steps': steps})

df = pd.DataFrame(rows)

avg_steps = df.groupby('ratio')['steps'].mean()

plt.figure(figsize=(10,6))
plt.plot(avg_steps.index, avg_steps.values, marker='o')

plt.xticks(sorted(df['ratio'].unique()))

plt.xlabel('Ratio')
plt.ylabel('Average Number of Steps')
plt.title('Avg. Steps vs Ratio: N=100, DLIS Heuristic')
plt.grid(True)
plt.show()