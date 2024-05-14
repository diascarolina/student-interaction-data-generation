import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# CSV data provided
csv_data = "../data/interaction_data.csv"

# Creating a DataFrame from CSV data
df = pd.read_csv(csv_data)

# Replace 'desired_username' with the username you want to select
desired_username = 'Manuella Martins'
selected_user_df = df[df['username'] == desired_username]

# Creating the graph
G = nx.DiGraph()

# Adding nodes and edges
for i, row in selected_user_df.iterrows():
    person = row['username']
    room = row['room']
    obj = row['object']
    activity = row['activity_type']
    detail = row['activity_type']

    # Add nodes
    G.add_node(person, type='Person', layer=0)
    G.add_node(room, type='Room', layer=1)
    if pd.notna(obj):
        G.add_node(obj, type='Object', layer=2)

    # Add edges
    if activity == 'movement':
        G.add_edge(person, room, type='Movement', detail=detail)
    elif activity == 'interaction':
        G.add_edge(room, obj, type='Interaction', detail=detail)

# Positioning nodes for visualization
pos = nx.multipartite_layout(G, subset_key="layer")

# Drawing the graph
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='k',
        linewidths=1, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'detail'),
                             font_color='red')
plt.title(f'Knowledge Graph of {desired_username} Activities')
plt.show()
