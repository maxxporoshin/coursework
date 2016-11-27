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


def check_subset(S, G, L=[]):
    if L and not check_pairs(L, S):
        return False
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
        for j in range(m):
            if G[i][j] == 1 and not trains[j]:
                continue
        for j in range(m):
            if G[i][j] == 1:
                trains[j] = True
                result.add(i)
        if False not in trains:
            return list(result)
    return []


def remove_vertix(S, G):
    for v in S:
        T = list(S)
        T.remove(v)
        if check_subset(T, G):
            return T
    return list(S)


def replace_2_vertices_with_1(S, G, L):
    subsets = itertools.combinations(S, 2)
    for subset in subsets:
        T = list(S)
        for v in subset:
            T.remove(v)
        for v in set(range(len(G))) - set(S):
            if check_subset(T + [v], G, L):
                return T + [v]
    return list(S)


def local_search(S, G, L):
    iterations = 0
    T, new_T = list(S), list()
    while len(T) > len(new_T):
        new_T = remove_vertix(T, G)
        new_T = replace_2_vertices_with_1(T, G, L) if new_T == T else new_T
        T = new_T
        iterations += 1
    print('Iterations:', iterations)
    return T


def replace_vertex_with_1(S, G, L):
    for v in S:
        T = list(S)
        T.remove(v)
        for x in set(range(len(G))) - set(S):
            if check_subset(T + [x], G, L):
                return T + [x]
    return list(S)


def replace_vertex_with_2(S, G, L):
    for v in S:
        T = list(S)
        T.remove(v)
        subsets = itertools.combinations(set(range(len(G))) - set(S), 2)
        for subset in subsets:
            pair = list(subset)
            if check_subset(T + pair, G, L):
                return T + pair
    return list(S)


def simulated_annealing(S, G, L, p1, p2):
    iterations = 0
    T, new_T = list(S), list()
    while True:
        new_T = remove_vertix(T, G)
        new_T = replace_2_vertices_with_1(T, G, L) if new_T == T else new_T
        if new_T == T:
            if random.random() < math.exp(-p1 * iterations):
                new_T = replace_vertex_with_1(T, G, L)
                if new_T != T:
                    T = new_T
                    iterations += 1
                    continue
            if random.random() < math.exp(-p2 * iterations):
                new_T = replace_vertex_with_2(T, G, L)
                if new_T != T:
                    T = new_T
                    iterations += 1
                    continue
            print('Iterations: ' + str(iterations))
            return T
        T = new_T
        iterations += 1


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
    greedy_solution = greedy(G, L)
    print(greedy_solution)
    print('{0:e}'.format(time.time() - t))
    print('Local search:')
    t = time.time()
    print(local_search(greedy_solution, G, L))
    print('{0:e}'.format(time.time() - t))
    print('Simulated annealing:')
    t = time.time()
    print(simulated_annealing(greedy_solution, G, L, 0.5, 0.5))
    print('{0:e}'.format(time.time() - t))


generate_and_solve_problem(50, 500, 0.7, 10)
