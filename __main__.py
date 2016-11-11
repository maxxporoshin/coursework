import random
import itertools
import time
import math


def generate_graph(n, m, p):
    G = [[1 if random.random() < p else 0 for j in range(m)] for i in range(n)]
    return G


def generate_pairs(amount, n):
    L = [[i, j] for i in range(n) for j in range(i + 1, n)]
    return random.sample(L, amount)


def check_pairs(L, S):
    for pair in L:
        if pair[0] in S and pair[1] in S:
            return False
    return True


def check_solvability_conditions(G, L):
    n = len(G)
    m = len(G[0])
    for j in range(m):
        stations = []
        for i in range(n):
            if G[i][j] == 1:
                stations.append(i)
        if len(stations) == 0:
            return False
    return True


def find_essential_subset(G):
    n = len(G)
    m = len(G[0])
    essentials = set()
    for j in range(m):
        stations = []
        for i in range(n):
            if G[i][j] == 1:
                stations.append(i)
        if len(stations) == 1:
                essentials.add(stations[0])
    return list(essentials)


def check_subset(S, G, L):
    m = len(G[0])
    all_connected = True
    for j in range(m):
        connected = False
        for i in S:
            if G[i][j] == 1:
                connected = True
        if not connected:
            all_connected = False
    if all_connected:
        if check_pairs(L, S):
            return True
    return False


def bruteforce(G, L):
    n = len(G)
    for k in range(1, n + 1):
        subsets = itertools.combinations(range(n), k)
        for S in subsets:
            if check_subset(S, G, L):
                return list(S)
    return []


def improved_bruteforce(G, L):
    n = len(G)
    if not check_solvability_conditions(G, L):
        return []
    essentials = find_essential_subset(G)
    if not check_pairs(L, essentials):
        return []
    if check_subset(essentials, G, L):
        return list(essentials)
    remaining = [i for i in range(n) if i not in essentials]
    for k in range(1, len(remaining) + 1):
        subsets = itertools.combinations(remaining, k)
        for subset in subsets:
            S = list(subset)
            S.extend(essentials)
            if check_subset(S, G, L):
                return S
    return []


def greedy(G, L):
    n = len(G)
    m = len(G[0])
    stations = [[i, 0] for i in range(n)]
    trains = [False for j in range(m)]
    for j in range(m):
        for i in range(n):
            stations[i][1] += G[i][j]
    stations.sort(key=lambda x: x[1], reverse=True)
    result = set()
    for i, v in stations:
        if not check_pairs(L, list(result) + [i]):
            continue
        all_trains_included = True
        for j in range(m):
            if G[i][j] == 1 and not trains[j]:
                all_trains_included = False
        if all_trains_included:
            continue
        for j in range(m):
            if G[i][j] == 1:
                trains[j] = True
                result.add(i)
        if False not in trains:
            return list(result)
    return []


def generate_and_solve_problem(n, m, p, l_amount):
    G = generate_graph(n, m, p)
    L = generate_pairs(l_amount, n)
    print('G:')
    print(G)
    print('L:')
    print(L)
    print('Bruteforce:')
    t = time.time()
    print(bruteforce(G, L))
    print('{0:e}'.format(time.time() - t))
    print('Improved bruteforce:')
    t = time.time()
    print(improved_bruteforce(G, L))
    print('{0:e}'.format(time.time() - t))
    print('Greedy:')
    t = time.time()
    print(greedy(G, L))
    print('{0:e}'.format(time.time() - t))


generate_and_solve_problem(10, 20, 0.5, 3)
