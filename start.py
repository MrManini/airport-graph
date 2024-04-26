from graph import Graph
import pandas as pd
import time

airports_df = pd.read_csv('airports.csv')
distances_df = pd.read_csv('distances.csv')

codes_df = airports_df['Code']
codes = codes_df.values.tolist()
G = Graph(codes)

for index, row in distances_df.iterrows():
    vi = row['Airport 1']
    vf = row['Airport 2']
    w = row['Distance']
    G.add_edge(vi, vf, w)

def is_real_airport(code: str) -> bool:
    info_df = airports_df[airports_df['Code'] == code]
    info = info_df.values.tolist()
    if info:
        return True
    return False

def show_airport_info(code: str) -> bool:
    info_df = airports_df[airports_df['Code'] == code]
    info = info_df.values.tolist()
    if info:
        print(f'Información del aerouerto {code}')
        print('...........................................-')
        print(f'Código IATA: {info[0][0]}')
        print(f'Nombre: {info[0][1]}')
        print(f'Ciudad: {info[0][2]}')
        print(f'País: {info[0][3]}')
        print(f'Latitud: {info[0][4]}')
        print(f'Longitud: {info[0][5]}')
        print('...........................................-')
        return True
    else:
        print(f'El aeropuerto {code} no está en el DataFrame.')
        return False

def biggest_airport_distances(code: str) -> None:
    global G
    top_airports, top_distances = G.top_10_longest_shortest_paths(code)
    print(f'Top 10 aeropuertos cuyo camino mínimo desde {code} es el más largo:')
    print('-----------------------------------------------------------------------')
    for i in range(10):
        print(f'{i+1}. {top_airports[i]} a {top_distances[i]} km.')
        show_airport_info(top_airports[i])
    print('-----------------------------------------------------------------------')

def path_to_second_airport(source: str, destination: str) -> None:
    global G
    path = G.find_path(source, destination)
    if path:
        print(f'Camino mínimo de {source} a {destination}:')
        path_string = ''
        for i in range(len(path) - 1):
            path_string += path[i] + ' -> '
        path_string += path[-1]
        print(path_string)
        distance = G.find_path_weight(path)
        print(f'Distancia total: {distance} km.')
        for i in range(len(path)):
            show_airport_info(path[i])
    else:
        print(f'No hay caminos que conecten de {source} a {destination}.')

code = 'kjaskjjks'
while code:
    code = input('Ingrese el código de un aeropuerto o presione enter para salir: ')
    if code:
        airport_exists = show_airport_info(code)
        if airport_exists:
            print('Opciones')
            print('1. Hallar el top 10 areopuertos con más largos caminos mínimos.')
            print(f'2. Buscar camino mínimo de {code} a otro aeropuerto.')
            print('Presione enter para no hacer ninguna opción.')
            selection = int(input())

            if selection == 1:
                if any(not updated for updated in G.updated):
                    start = time.time()
                    for i in range(G.n):
                        if not G.updated[i]:
                            G.dijkstra(G.names[i])
                            done = G.updated.count(True)
                            print(f'Análisis {round(done/G.n * 100, 2)}% terminado. ({done}/{G.n})')
                    end = time.time()
                    print(f'Tiempo total de ejecución: {end - start}.')
                biggest_airport_distances(code)
            elif selection == 2:
                destination = input('Ingrese el código de aeropuerto destino: ')
                if is_real_airport(destination):
                    ver_index = G.names.index(code)
                    if not G.updated[ver_index]:
                        G.dijkstra(code)
                    path_to_second_airport(code, destination)
                else:
                    print('No es un código válido.')
        else:
            print(f'{code} no es un aeropuerto válido.')
    