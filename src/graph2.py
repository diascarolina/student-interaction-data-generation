import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Sample data
data = {
    'name': ["Evelyn da Paz"] * 7,
    'id': [3] * 7,
    'timestamp': [
        "2024-07-16 00:03:30",
        "2024-07-16 00:07:22",
        "2024-07-16 00:12:22",
        "2024-07-16 00:20:30",
        "2024-07-16 00:23:46",
        "2024-07-16 00:27:52",
        "2024-07-16 00:31:43"
    ],
    'type': [
        "interaction", "interaction", "interaction",
        "movement", "interaction", "interaction", "interaction"
    ],
    'location': ["Classroom", "Classroom", "Classroom", "Café", "Café", "Café", "Café"],
    'object': ["Desk", "Book", "Book", "", "Table", "Chair2", "Student"],
    'duration': [
        "00:03:30", "00:03:52", "00:05:00",
        "00:08:08", "00:03:16", "00:04:06", "00:03:51"
    ],
    'description': [
        "Interacted with Desk",
        "Interacted with Book",
        "Interacted with Book",
        "Moved from Classroom to Café",
        "Interacted with Table",
        "Interacted with Chair2",
        "Interacted with Student"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Initialize directed graph
G = nx.DiGraph()

# Add the student as a node
student = "Evelyn da Paz"
G.add_node(student, type='Person')

# Add nodes and edges
for index, row in df.iterrows():
    location = row['location']
    obj = row['object']
    interaction_type = row['type']
    description = row['description']

    # Add location as a node if not already added
    if location not in G:
        G.add_node(location, type='Location')

    # If there's an object, add it as a node and create an edge
    if obj:
        if obj not in G:
            G.add_node(obj, type='Object')
        G.add_edge(student, obj, label=description)
        G.add_edge(obj, location, label=description)
    elif interaction_type == "movement":
        # Create an edge between locations for movement
        if 'Moved from' in description:
            from_location, to_location = description.split('Moved from ')[1].split(' to ')
            if from_location not in G:
                G.add_node(from_location, type='Location')
            if to_location not in G:
                G.add_node(to_location, type='Location')
            G.add_edge(student, to_location, label=description)

# Draw the graph
pos = nx.spring_layout(G)  # positions for all nodes

plt.figure(figsize=(12, 10))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10,
        font_weight="bold", edge_color="gray")

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# Show plot
plt.title("User Interaction Knowledge Graph")
plt.show()
