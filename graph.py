from typing import List, Any
import time

class Graph:

    def __init__(self, names: List[Any], directed: bool = False) -> None:
        self.names = names
        self.n = len(self.names)
        self.directed = directed
        self.ad_mtrx: List[List[float]] = [[0 for i in range(self.n)] for j in range(self.n)]
        self.cost_mtrx: List[List[float]] = [[float('inf') for i in range(self.n)] for j in range(self.n)]
        self.path_mtrx: List[List[Any]] = [list(self.names) for _ in range(self.n)]
        for i in range(self.n):
            self.cost_mtrx[i][i] = 0
            self.path_mtrx[i][i] = '-'
        self.updated = [False] * self.n

    def add_edge(self, initial_v: Any, final_v: Any, weight: float) -> bool:
        vi = self.names.index(initial_v)
        vf = self.names.index(final_v)
        if not ((0 <= vi < self.n) and (0 <= vf < self.n)):
            return False
        if self.directed:
            self.ad_mtrx[vi][vf] = weight
            self.cost_mtrx[vi][vf] = weight
            return True
        self.ad_mtrx[vi][vf] = self.ad_mtrx[vf][vi] = weight
        self.cost_mtrx[vi][vf] = weight
        self.cost_mtrx[vf][vi] = weight
        return True

    def dijkstra(self, vertex: Any) -> None:
        print(f'Ejecutando algoritmo Dijkstra con {vertex}...')
        start = time.time()
        known_list = [False for _ in range(self.n)]
        cost_list = [float('inf') for _ in range(self.n)]
        path_list = ['-' for _ in range(self.n)]
        ver_index = self.names.index(vertex)
        cost_list[ver_index] = 0
        min_cost = 0

        while any(not known for known in known_list) and min_cost < float('inf'):
            not_known_costs = [cost for i, cost in enumerate(cost_list) if not known_list[i]]
            min_cost = min(not_known_costs)
            min_index = cost_list.index(min_cost)
            last_vertex = self.names[min_index]
            known_list[min_index] = True
            ad_list = self.ad_mtrx[min_index]
            
            for i in range(self.n):
                if ad_list[i] != 0 and min_cost + ad_list[i] < cost_list[i]:
                    cost_list[i] = min_cost + ad_list[i]
                    path_list[i] = last_vertex
        
        self.cost_mtrx[ver_index] = cost_list
        self.path_mtrx[ver_index] = path_list
        self.updated[ver_index] = True
        end = time.time()
        print(f'Tiempo de ejecución: {end-start}')
    
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
        self.updated = [True] * self.n
        print(f'Tiempo de ejecución de Floyd-Warshall: {finish-start}')

    def top_10_longest_shortest_paths(self, vertex: Any) -> List[Any]:
        i = self.names.index(vertex)
        path_costs = [cost for cost in self.cost_mtrx[i] if cost < float('inf')]
        path_costs.sort(reverse=True)
        top_10 = path_costs[:10]
        indices = [self.cost_mtrx[i].index(cost) for cost in top_10]
        names = [self.names[index] for index in indices]
        return names, top_10

    def find_path(self, vertex1: Any, vertex2: Any) -> List[Any]:
        index1 = self.names.index(vertex1)
        index2 = self.names.index(vertex2)
        if self.cost_mtrx[index1][index2] != float('inf'):
            if vertex1 == vertex2:
                return [vertex1]
            else:
                mid_point = self.path_mtrx[index1][index2]
                path = self.find_path(vertex1, mid_point)
                path.append(vertex2)
                return path
        else:
            return []

    def find_path_weight(self, path: List[Any]) -> float:
        total_weight = 0
        for i in range(len(path)-1):
            index1 = self.names.index(path[i])
            index2 = self.names.index(path[i+1])
            total_weight += self.ad_mtrx[index1][index2]
        return total_weight