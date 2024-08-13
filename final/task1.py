import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

plt.figure(figsize=(12, 9))

# Add nodes
nodes = ["Hyde Park Corner", "Green Park", "Piccadilly Circus", "Leicester Square", "Covent Garden", "Holborn"]
G.add_nodes_from(nodes)

# Add edges with distances
edges = [
    ("Hyde Park Corner", "Green Park", 0.6),
    ("Green Park", "Piccadilly Circus", 0.4),
    ("Piccadilly Circus", "Leicester Square", 0.3),
    ("Leicester Square", "Covent Garden", 0.2),
    ("Covent Garden", "Holborn", 0.5)
]
G.add_weighted_edges_from(edges)

# Define positions for the nodes
positions = {
    'Hyde Park Corner': (0, 0),
    'Green Park': (1, 1),
    'Piccadilly Circus': (3, 1),
    'Leicester Square': (4.8, 1),
    'Covent Garden': (5.5, 1.3),
    'Holborn': (7, 2)
}

# Define positions for the nodes labels (x, y, rotation)
label_positions = {
    'Hyde Park Corner': (0, -0.1, 0),
    'Green Park': (1, 0.9, 0),
    'Piccadilly Circus': (3, 0.9, 0),
    'Leicester Square': (4.8, 0.9, 0),
    'Covent Garden': (5.5, 1.2, 0),
    'Holborn': (7, 1.9, 0)
}

# Draw the graph
nx.draw_networkx_nodes(G, positions, node_color="blue", node_size=500)
nx.draw_networkx_edges(G, positions, width=2, label='Piccadilly Line', edge_color="blue")

# Add node labels
for node, (x, y, rotation) in label_positions.items():
    plt.text(x, y, node, fontsize=10, ha="center", va="center", fontweight="bold", rotation=rotation)

# Add edge labels with distances
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels)

# Add title and legend
plt.title("Piccadilly Line")
plt.legend(ncol=1, fontsize=10, loc="lower right")

# Show the plot
plt.show()
