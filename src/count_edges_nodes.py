import pandas as pd
import networkx as nx

# Sample data
df = pd.read_csv("../data/simulation_data_200u_200d.csv")

# Create a directed graph
G = nx.DiGraph()

# Process each row in the DataFrame
for index, row in df.iterrows():
    student = row['username']
    room = row['room']
    object_ = row['object']

    # Add student and room to nodes
    G.add_node(student, type='Student')
    if room:
        G.add_node(room, type='Room')

    # Add object to nodes if it's an interaction
    if row['activity_type'] == 'interaction' and object_:
        G.add_node(object_, type='Object')
        G.add_edge(student, object_, type='interaction', timestamp=row['timestamp'])

    # Add movement edges
    if row['activity_type'] == 'movement':
        if "Moved from" in row['details']:
            from_room = row['details'].split("Moved from ")[1].split(" to ")[0]
            to_room = row['details'].split("Moved from ")[1].split(" to ")[1]
            G.add_node(from_room, type='room')
            G.add_node(to_room, type='room')
            G.add_edge(from_room, to_room, type='movement', timestamp=row['timestamp'])
        else:
            to_room = row['room']
            G.add_edge(student, to_room, type='movement', timestamp=row['timestamp'])

# Calculate the number of nodes and edges
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

print(f'{num_nodes=} and {num_edges=}')
