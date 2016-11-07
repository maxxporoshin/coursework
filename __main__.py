import random
import itertools


class Station:
    def __init__(self, index, trains=[]):
        self.index = index
        self.trains = trains


def print_stations(S):
    for station in S:
        print(station.index, station.trains)


def generate_graph(n, m, p):
    G = [Station(i) for i in range(n)]
    for station in G:
        station.trains = [1 if random.random() < p else 0 for j in range(m)]
    return G


def generate_pairs(amount, n):
    L = [[i, j] for i in range(n) for j in range(i + 1, n)]
    return random.sample(L, amount)


def check_pairs(L, S):
    indeces = []
    for station in S:
        indeces.append(station.index)
    for pair in L:
        if pair[0] in indeces and pair[1] in indeces:
            return False
    return True


def bruteforce(G, L):
    m = len(G[0].trains)
    for k in range(2, len(G) + 1):
        subsets = itertools.combinations(G, k)
        for S in subsets:
            all_connected = True
            for j in range(m):
                connected = False
                for station in S:
                    if station.trains[j] == 1:
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
    print_stations(G)
    print('L:')
    print(L)
    print('Bruteforce:')
    print_stations(bruteforce(G, L))


generate_and_solve_problem(3, 5, 0.5, 1)
