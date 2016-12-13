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


def there_are_ghost_trains(G):
    n = len(G)
    m = len(G[0])
    for j in range(m):
        ghost = True
        for i in range(n):
            if G[i][j] == 1:
                ghost = False
                break
        if ghost:
            return True
    return False


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
    # print('Iterations:', iterations)
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
            # print('Iterations: ' + str(iterations))
            return T
        T = new_T
        iterations += 1


# def generate_and_solve_problem(n, m, p, l_amount):
#     G = generate_graph(n, m, p)
#     L = generate_pairs(l_amount, n)
#     print('G:')
#     print(G)
#     print('L:')
#     print(L)
#     print('Bruteforce:')
#     t = time.time()
#     print(bruteforce(G, L))
#     print('{0:e}'.format(time.time() - t))
#     print('Greedy:')
#     t = time.time()
#     greedy_solution = greedy(G, L)
#     print(greedy_solution)
#     print('{0:e}'.format(time.time() - t))
#     print('Local search:')
#     t = time.time()
#     print(local_search(greedy_solution, G, L))
#     print('{0:e}'.format(time.time() - t))
#     print('Simulated annealing:')
#     t = time.time()
#     print(simulated_annealing(greedy_solution, G, L, 0.5, 0.5))
#     print('{0:e}'.format(time.time() - t))


def generate_and_solve_problem(n, m, p, l_amount, iters):
    brute = open('brute.txt', 'w')
    greed = open('greed.txt', 'w')
    local = open('local.txt', 'w')
    annealing = open('annealing.txt', 'w')
    brute_t = open('brute_t.txt', 'w')
    greed_t = open('greed_t.txt', 'w')
    local_t = open('local_t.txt', 'w')
    annealing_t = open('annealing_t.txt', 'w')
    i = iters
    while i != 0:
        G = generate_graph(n, m, p)
        if there_are_ghost_trains(G):
            print('ghost')
            continue
        L = generate_pairs(l_amount, n)
        print('Iteration ' + str(iters - i))
        t = time.time()
        brute.write(str(len(bruteforce(G, L))) + '\n')
        brute_t.write('{:2f}'.format(time.time() - t) + '\n')
        print('|', end='')
        t = time.time()
        greedy_solution = greedy(G, L)
        greed.write(str(len(greedy_solution)) + '\n')
        greed_t.write('{:2f}'.format(time.time() - t) + '\n')
        print('|', end='')
        t = time.time()
        local.write(str(len(local_search(greedy_solution, G, L))) + '\n')
        local_t.write('{:2f}'.format(time.time() - t) + '\n')
        print('|', end='')
        t = time.time()
        annealing.write(str(len(simulated_annealing(greedy_solution, G, L, 0.5, 0.5))) + '\n')
        annealing_t.write('{:2f}'.format(time.time() - t) + '\n')
        print('|', end='')
        print()
        i -= 1
    brute.close()
    brute_t.close()
    greed.close()
    greed_t.close()
    local.close()
    local_t.close()
    annealing.close()
    annealing_t.close()


generate_and_solve_problem(25, 100, 0.25, 10, 10)
