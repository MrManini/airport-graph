import pandas as pd
from graph import Graph

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

G.floyd_warshall()
df = pd.DataFrame(G.cost_mtrx)

df.to_csv('cost_matrix.csv', index=False, header=False)