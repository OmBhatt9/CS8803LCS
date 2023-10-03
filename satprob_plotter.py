import json
import pandas as pd
import matplotlib.pyplot as plt

filename = 'dlis100.json'

with open(filename, 'r') as file:
    data = json.load(file)

rows = []
for ratio, sub_dict in data.items():
    for int_value, (sat_status, steps) in sub_dict.items():
        rows.append({'ratio': float(ratio), 'int_value': int(int_value), 'sat_status': sat_status, 'steps': steps})

df = pd.DataFrame(rows)

sat_counts = df[df['sat_status'] == 'SAT'].groupby('ratio')['sat_status'].count()

total_counts = df.groupby('ratio')['sat_status'].count()

prob_sat = sat_counts / total_counts
prob_sat = prob_sat.fillna(0)

plt.figure(figsize=(10,6))
plt.plot(prob_sat.index, prob_sat.values, marker='o')

plt.xticks(sorted(df['ratio'].unique()), rotation=45)
plt.yticks([i/10.0 for i in range(11)])

plt.xlabel('Ratio')
plt.ylabel('Probability of Satisfiability')
plt.title('Probability of Satisfiability vs Ratio: N=100, DLIS Heuristic')
plt.grid(True)
plt.show()

