import random
import time
import os
import numpy as np
import json
from collections import defaultdict, Counter

def twoclause_heuristic(F):
    literal_counts = {}
    two_clauses = [clause for clause in F if len(clause) == 2]
    for clause in two_clauses:
        for literal in clause:
            literal_counts[literal] = 1 if literal not in literal_counts else literal_counts[literal] + 1
    if not literal_counts:
        return F[0][0]
    chosen = max(literal_counts, key=literal_counts.get)
    return chosen

##############################################################################################################

# Jeroslow-Wang Heuristic (From Interim Report, Discarded)
def jw_heuristic(F):
    scores = {}
    for clause in F:
        for literal in clause:
            if literal not in scores:
              scores[literal] = 0
    for clause in F:
        impact = 1 / 2**len(clause)
        for literal in clause:
            scores[literal] += impact
    chosen = max(scores, key=scores.get)
    return chosen

# DLIS Heuristic (Custom Heuristic)
def dlis_heuristic(formula, assignments):
    literal_count = defaultdict(int)
    
    for clause in formula:
        if any(literal in assignments and assignments[literal] for literal in clause):
            continue
        
        for literal in clause:
            neglit = literal[1:] if literal.startswith('-') else '-' + literal
            if literal not in assignments and neglit not in assignments:
                literal_count[literal] += 1
    
    if not literal_count:
        return None
    
    return max(literal_count, key=literal_count.get)

##############################################################################################################

def random_heuristic(F):
    chosenclause = random.choice(F)
    chosen = random.choice(chosenclause)
    return chosen

##############################################################################################################

def unit_prop(formula, assignments):
    f = formula.copy()
    # while a unit clause exists in the formula
    while any(len(clause) == 1 for clause in f):
        # select the first available unit clause
        unit_clause = next(clause for clause in f if len(clause) == 1)
        literal = unit_clause[0]
        negliteral = "-" + literal if "-" not in literal else literal[1:]
        # remove all clauses containing the unit literal
        f = [c for c in f if literal not in c]
        # shorten all clauses containing the negation of the unit literal
        f = [[l for l in c if l != negliteral] for c in f]
        # add the unit literal to the assignments
        if "-" in literal:
            assignments[literal[1:]] = False
        else:
            assignments[literal] = True
    return f, assignments

##############################################################################################################

def pure_elim(formula, assignments):
    f = formula.copy()
    pure_literals = find_pure_literals(f, assignments)
    # iterate through the pure literals
    for p in pure_literals:
        # remove all clauses containing the pure literal
        f = [c for c in f if p not in c]
        # add the pure literal to the assignments
        if "-" in p:
            assignments[p[1:]] = False
        else:
            assignments[p] = True
    return f, assignments

##############################################################################################################

def find_pure_literals(formula, assignments):
    # count the occurrences of each literal in the formula
    literals = []
    for clause in formula:
        for literal in clause:
            literals.append(literal)
    # find literals that occur in only one polarity and are not assigned a value
    pure_literals = []
    for literal in literals:
        neg_literal = "-" + literal if "-" not in literal else literal[1:]
        if literal not in assignments and neg_literal not in assignments and neg_literal not in literals:
            pure_literals.append(literal)
   
    return pure_literals

##############################################################################################################

# DPLL algorithm, adapted from https://shorturl.at/ewO16 and https://cs.brown.edu/courses/cs195y/2017/labs/lab-4.html

def dpll(F, assignments, heuristic):
    global steps
    
    steps += 1

    # make a copy of assignments
    new_assignments = {k: v for k, v in assignments.items()}
    # perform unit propagation and pure literal elimination
    formula, assignments = unit_prop(F, new_assignments)
    formula, assignments = pure_elim(formula, assignments)

    # if the formula has empty clauses, it is unsatisfiable
    if [] in formula:
        return "UNSAT"
    # if all clauses have atleast one literal that is assigned true, the whole thing is satisfied
    if all(any(l in assignments and assignments[l] for l in clause) for clause in formula):
        # return "SAT"
        return assignments
    
    # choose a literal in case neither of the above conditions are true
    if heuristic == "random":
        chosen = random_heuristic(formula)
    if heuristic == "twoclause":
        chosen = twoclause_heuristic(formula)
    if heuristic == "jw":
        chosen = jw_heuristic(formula)
    if heuristic == "dlis":
        chosen = dlis_heuristic(formula, assignments )

    if chosen:
        negchosen = "-" + chosen if "-" not in chosen else chosen[1:]
        new_assignments = {k: v for k, v in assignments.items()}

        # add chosen literal to assignments
        if "-" in chosen:
            new_assignments[chosen[1:]] = False
        else:
            new_assignments[chosen] = True

        # recursively call dpll with the chosen literal set to true
        result = dpll(formula + [[chosen]], new_assignments, heuristic)
        if result != "UNSAT":
            return result
        
        # if that didn't work, try setting the negation of the chosen literal to true with a new copy of assignments
        new_assignments = {k: v for k, v in assignments.items()}

        # add negation of chosen literal to assignments
        if "-" in negchosen:
            new_assignments[negchosen[1:]] = False
        else:
            new_assignments[negchosen] = True

        # recursively call dpll with the negation of the chosen literal set to true
        result = dpll(formula + [[negchosen]], new_assignments, heuristic)
        if result != "UNSAT":
            return result     
        
    return "UNSAT"

##############################################################################################################

path = "n130_cnf_formulas"

# results100random = {}
# results100twoclause = {}
# results100jw = {}
# results100dlis = {}

results130random = {}
# results130twoclause = {}
# results130jw = {}
# results130dlis = {}

for j in np.arange(3.0, 6.2, 0.2):
    print("starting " + str(round(j, 1)))
    curresultsrandom = {}
    # curresultstwoclause = {}
    # curresultsjw = {}
    # curresultsdlis = {}
    for i in range(100):
        if i % 25 == 0: print("starting " + str(i))
        filename = os.path.join(path+str(round(j, 2)), f'random_3cnf_{i}.cnf')
        file = open(filename, "r")
        form = []
        curr = []
        for line in file:
            if line[0] == "c" or line[0] == "0" or line[0] == "%":
                continue
            if line[0] == "p":
                contents = line.split()
                var_no = int(contents[-2])
                clause_no = int(contents[-1])
            else:
                for n in line.split():
                    if n == "0":
                        form.append(curr)
                        curr = []
                    elif n != "0": curr.append(str(n))
        if curr != []: form.append(curr)

        steps = 0
        # restarts = 0
        # curr_steps = 0
        # max_steps = 15000
        # print("original formula: " + str(form))

        assignments = {}
        result1 = dpll(form, assignments, heuristic="random")
        # result2 = dpll(form, assignments, heuristic="twoclause")
        # result3 = dpll(form, assignments, heuristic="jw")
        # result4 = dpll(form, assignments, heuristic="dlis")

        # if result1 == "RESTART":
        #     restarts += 1
        #     print("RESTART")
        #     curr_steps = 0
        #     continue

        if result1 != "UNSAT":
            curresultsrandom[i] = ("SAT", steps)
        else:
            curresultsrandom[i] = ("UNSAT", steps)  

        # if result2 != "UNSAT":
        #     curresultstwoclause[i] = ("SAT", steps)
        # else:
        #     curresultstwoclause[i] = ("UNSAT", steps) 

        # if result3 != "UNSAT":
        #     curresultsjw[i] = ("SAT", steps)
        # else:
        #     curresultsjw[i] = ("UNSAT", steps)

        # if result4 != "UNSAT":
        #     curresultsdlis[i] = ("SAT", steps)
        # else:
        #     curresultsdlis[i] = ("UNSAT", steps)
            
    # results100random[round(j, 1)] = curresultsrandom
    # results100twoclause[round(j, 1)] = curresultstwoclause
    # results100jw[round(j, 1)] = curresultsjw
    # results100dlis[round(j, 1)] = curresultsdlis

    results130random[round(j, 1)] = curresultsrandom
    # results130twoclause[round(j, 1)] = curresultstwoclause
    # results130jw[round(j, 1)] = curresultsjw
    # results130dlis[round(j, 1)] = curresultsdlis

# with open('random100.json', 'w+') as f:
#     json.dump(results100random, f)

# with open('twoclause100.json', 'w+') as f:
#     json.dump(results100twoclause, f)

# with open('jw100.json', 'w+') as f:
#     json.dump(results100jw, f)

# with open('dlis100.json', 'w+') as f:
#     json.dump(results100dlis, f)

with open('random130.json', 'w+') as f:
    json.dump(results130random, f)

# with open('twoclause130.json', 'w+') as f:
#     json.dump(results130twoclause, f)

# with open('jw130.json', 'w+') as f:
#     json.dump(results130jw, f)

# with open('dlis130.json', 'w+') as f:
#     json.dump(results130dlis, f)

##############################################################################################################

### INTERIM REPORT CODE ###

# # DIMACS File reader and parser into list of lists of integer strings
# print("Enter the word random, twoclause, or jw or dlis to choose a heuristic: ")
# heuristic = input()
# file = open(r"einstein.cnf", "r")
# form = []
# curr = []
# for line in file:
#     if line[0] == "c" or line[0] == "0" or line[0] == "%":
#         continue
#     if line[0] == "p":
#         contents = line.split()
#         var_no = int(contents[-2])
#         clause_no = int(contents[-1])
#     else:
#         for n in line.split():
#             if n == "0":
#                 form.append(curr)
#                 curr = []
#             elif n != "0": curr.append(str(n))
# if curr != []: form.append(curr)

# steps = 0
# # print("original formula: " + str(form))

# assignments = {}
# result = dpll(form, assignments, heuristic)
# if result != "UNSAT":
#     #sort dict by key for easier reading
#     res = {k: result[k] for k in sorted(result, key=lambda x: int(x))}
#     print(res)
    
# else:
#     print("result: " + str(result))
    
# print("Steps taken: " + str(steps))

