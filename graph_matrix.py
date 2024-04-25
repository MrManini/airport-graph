from pprint import pprint
from queue import Queue
from typing import List, Tuple
from pprint import pprint
import time

class GraphMatrix:

    def __init__(self, names: List[str]) -> None:
        self.names = names
        self.n = len(self.names)
        self.ad_mtrx: List[List[float]] = [[0 for i in range(self.n)] for j in range(self.n)]
        self.cost_mtrx: List[List[float]] = [[float('inf') for i in range(self.n)] for j in range(self.n)]
        self.path_mtrx: List[List[str]] = [list(self.names) for _ in range(self.n)]
        for i in range(self.n):
            self.cost_mtrx[i][i] = 0
            self.path_mtrx[i][i] = '-'

    def add_edge(self, initial_v: str, final_v: str, weight: float) -> bool:
        vi = self.names.index(initial_v)
        vf = self.names.index(final_v)
        if not ((0 <= vi < self.n) and (0 <= vf < self.n)):
            return False
        self.ad_mtrx[vi][vf] = self.ad_mtrx[vf][vi] = weight
        self.cost_mtrx[vi][vf] = weight
        self.cost_mtrx[vf][vi] = weight
        return True

    def floyd_warshall(self) -> None:
        print(f'Ejecutando algoritmo Floyd-Warshall...')
        start = time.time()
        for i in range(self.n):
            print(i)
            from_x = self.cost_mtrx[i]
            to_x = [row[i] for row in self.cost_mtrx]
            for j in range(self.n):
                if 0 < to_x[j] < float('inf'):
                    for k in range(self.n):
                        if (to_x[j] + from_x[k]) < self.cost_mtrx[j][k]:
                            self.cost_mtrx[j][k] = to_x[j] + from_x[k]
                            self.path_mtrx[j][k] = self.names[i]
        finish = time.time()
        print(f'Tiempo de ejecución de Floyd-Warshall: {finish-start}')

    def top_10_longest_shortest_paths(self, vertex: str) -> List[str]:
        i = self.names.index(vertex)
        path_costs = [cost for cost in self.cost_mtrx[i] if cost < float('inf')]
        path_costs.sort(reverse=True)
        top_10 = path_costs[:10]
        indices = [self.cost_mtrx[i].index(cost) for cost in top_10]
        names = [self.names[index] for index in indices]
        return names, top_10

    def find_path(self, vertex1: str, vertex2: str) -> List[str]:
        index1 = self.names.index(vertex1)
        index2 = self.names.index(vertex2)
        if self.cost_mtrx[index1][index2] != float('inf'):
            if vertex2 == self.path_mtrx[index1][index2]:
                return [vertex1, vertex2]
            else:
                mid_point = self.path_mtrx[index1][index2]
                path = self.find_path(vertex1, mid_point)
                path.append(vertex2)
                return path
        else:
            return []