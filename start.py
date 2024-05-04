from graph import Graph
import pandas as pd
import simplekml
import os
import subprocess

print('Cargando datos...')
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
        kml = simplekml.Kml()
        for i in range(len(path)):
            airport_coords = (
                airports_df[airports_df['Code'] == path[i]]['Longitude'].values[0],
                airports_df[airports_df['Code'] == path[i]]['Latitude'].values[0],
                1000
                )
            point = kml.newpoint(name=path[i], coords=[airport_coords])
            point.style.iconstyle.icon.href = 'http://www.gstatic.com/mapspro/images/stock/1417-trans-airport.png'
            point.style.iconstyle.scale = 2
            point.style.labelstyle.scale = 3
            if i > 0:
                last_coords = (
                    airports_df[airports_df['Code'] == path[i-1]]['Longitude'].values[0],
                    airports_df[airports_df['Code'] == path[i-1]]['Latitude'].values[0],
                    1000
                    )
                distance_between_airports = G.find_path_weight([path[i-1], path[i]])
                line = kml.newlinestring(name=f'{path[i-1]} - {path[i]}', coords=[last_coords, airport_coords])
                line.style.linestyle.width = 3
                line.altitudemode = simplekml.AltitudeMode.clamptoground
                line.tessellate = 1
                line.style.linestyle.color = simplekml.Color.red
                line.description = f'Distancia: {round(distance_between_airports)} km.'
            show_airport_info(path[i])
        return kml
    else:
        print(f'No hay caminos que conecten de {source} a {destination}.')

code = 'kjaskjjks'
while code:
    code = input('Ingrese el código de un aeropuerto o presione enter para salir: ')
    code = code.upper()
    if code:
        airport_exists = show_airport_info(code)
        if airport_exists:
            kml = simplekml.Kml()
            airport_coords = [
                (airports_df[airports_df['Code'] == code]['Longitude'].values[0],
                  airports_df[airports_df['Code'] == code]['Latitude'].values[0])
                  ]
            source = kml.newpoint(name=code, coords=airport_coords)
            source.style.iconstyle.icon.href = 'http://www.gstatic.com/mapspro/images/stock/1417-trans-airport.png'
            kml.save('graph_map.kml')
            kml_path = os.path.abspath('graph_map.kml')
            #subprocess.run(['google-earth-pro', kml_path])
            print('Opciones')
            print('1. Hallar el top 10 areopuertos con más largos caminos mínimos.')
            print(f'2. Buscar camino mínimo de {code} a otro aeropuerto.')
            print('Presione enter para no hacer ninguna opción.')
            try:
                selection = int(input())
                ver_index = G.names.index(code)
                if not G.updated[ver_index]:
                    G.dijkstra(code)
                if selection == 1:
                    biggest_airport_distances(code)
                elif selection == 2:
                    destination = input('Ingrese el código de aeropuerto destino: ')
                    destination = destination.upper()
                    if is_real_airport(destination):
                        path_kml = path_to_second_airport(code, destination)
                        path_kml.save('path_map.kml')
                        kml_path = os.path.abspath('path_map.kml')
                        subprocess.run(['google-earth-pro', kml_path])
                    else:
                        print(f'{destination} no es un aeropuerto válido.')
            except Exception as e:
                print(e)
                print('Ingrese una opción válida.')
        else:
            print(f'{code} no es un aeropuerto válido.')
    