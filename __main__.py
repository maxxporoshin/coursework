import random
import itertools


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


def bruteforce(G, L):
    n = len(G)
    m = len(G[0])
    for k in range(2, n + 1):
        subsets = itertools.combinations(range(n), k)
        for S in subsets:
            all_connected = True
            for j in range(m):
                connected = False
                for i in range(n):
                    if G[i][j] == 1:
                        connected = True
                if not connected:
                    all_connected = False
            if all_connected:
                if check_pairs(L, S):
                    return S
    return []


def generate_and_solve_problem(n, m, p, l_amount):
    G = generate_graph(n, m, p)
    L = generate_pairs(1, n)
    print('G:')
    print(G)
    print('L:')
    print(L)
    print('Bruteforce:')
    print(bruteforce(G, L))


generate_and_solve_problem(3, 5, 0.5, 1)
