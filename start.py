from graph_matrix import GraphMatrix
import pandas as pd

airports_df = pd.read_csv('airports.csv')
distances_df = pd.read_csv('distances.csv')

codes_df = airports_df['Code']
codes = codes_df.values.tolist()
G = GraphMatrix(codes)

for index, row in distances_df.iterrows():
    vi = row['Airport 1']
    vf = row['Airport 2']
    w = row['Distance']
    G.add_edge(codes.index(vi), codes.index(vf), w)

distances_matrix = G.D
