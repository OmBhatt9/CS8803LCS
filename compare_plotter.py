import json
import pandas as pd
import matplotlib.pyplot as plt

filename1 = 'dlis130.json'
filename2 = 'twoclause130.json'

with open(filename1, 'r') as file:
    data1 = json.load(file)

with open(filename2, 'r') as file:
    data2 = json.load(file)

# Convert to DataFrames
def create_dataframe(data):
    rows = []
    for ratio, sub_dict in data.items():
        for int_value, (sat_status, steps) in sub_dict.items():
            rows.append({'ratio': float(ratio), 'int_value': int(int_value), 'sat_status': sat_status, 'steps': steps})
    return pd.DataFrame(rows)

df1 = create_dataframe(data1)
df2 = create_dataframe(data2)

avg_steps1 = df1.groupby('ratio')['steps'].mean()
avg_steps2 = df2.groupby('ratio')['steps'].mean()

plt.figure(figsize=(10,6))

plt.plot(avg_steps1.index, avg_steps1.values, marker='o', label='DLIS Heuristic')

plt.plot(avg_steps2.index, avg_steps2.values, marker='s', label='2-Clause Heuristic')

all_ratios = sorted(set(df1['ratio'].unique()).union(set(df2['ratio'].unique())))
plt.xticks(all_ratios, rotation=45)

plt.xlabel('Ratio')
plt.ylabel('Average Number of Steps')
plt.title('N=130: Average Number of Steps vs Ratio by Heuristic')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()


