import dynetx as dn
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Assuming 'csv_data' points to the path of your CSV file
csv_data = "../data/interaction_data.csv"

# Load the data
df = pd.read_csv(csv_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter for a specific username
desired_username = 'Manuella Martins'
selected_user_df = df[df['username'] == desired_username]

# Create the dynamic graph
DG = dn.DynDiGraph()

# Add nodes and dynamic edges
for index, row in selected_user_df.iterrows():
    person = row['username']
    room = row['room']
    obj = row['object']
    activity = row['activity_type']
    timestamp = row['timestamp']

    # Add nodes (you might want to manage nodes dynamically as well)
    DG.add_node(person)
    DG.add_node(room)
    if pd.notna(obj):
        DG.add_node(obj)

    # Add edges with the time as an interval (here using the same time for start and end for simplicity)
    if activity == 'movement':
        DG.add_interaction(person, room, t_from=timestamp, t_to=timestamp)
    elif activity == 'interaction':
        DG.add_interaction(room, obj, t_from=timestamp, t_to=timestamp)

# For visualization, extract a static snapshot at a specific time
snapshot_time = pd.to_datetime('2024-01-01 00:06:04')
G_snapshot = DG.interactions_at(snapshot_time)

# Draw the snapshot
plt.figure(figsize=(12, 8))
nx.draw(G_snapshot, with_labels=True, node_color='skyblue', edge_color='k', node_size=2000, linewidths=1, font_size=12)
plt.title(f'Snapshot of {desired_username} Activities at {snapshot_time}')
plt.show()