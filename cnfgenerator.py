import random
import os
import numpy as np

def generate_3cnf(N, L, filename):
    with open(filename, 'w+') as file:
        file.write('c Random 3-CNF formula\n')
        file.write(f'p cnf {N} {L}\n')

        for _ in range(L):
            clause = random.sample(range(1, N + 1), 3)
            clause = [literal if random.random() < 0.5 else -literal for literal in clause]
            clause_str = ' '.join(map(str, clause)) + ' 0\n'
            file.write(clause_str)

path = "n100_cnf_formulas"

N = 100

for i in range(100):
    for j in np.arange(3.0, 6.2, 0.2):
        os.makedirs(path+str(j), exist_ok=True)
        filename = os.path.join(path+str(j), f'random_3cnf_{i}.cnf')
        generate_3cnf(N, int(N * j), filename)