import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the data from the CSV file for road distances
file_path = 'process3.csv'
print(f"Loading data from: {file_path}")
data = pd.read_csv(file_path, encoding='latin1')

# debug
print("Data head:")
print(data.head())
print()


# Load station coordinates 
coordinates_file = 'stations.csv'
print(f"Loading coordinates from: {coordinates_file}")
coordinates_data = pd.read_csv(coordinates_file)

# Print initial insights into the coordinates data
print("Coordinates head:")
print(coordinates_data.head())
print()

# Create a dictionary of station coordinates
station_coordinates = {}
for _, row in coordinates_data.iterrows():
    station_coordinates[row['Station']] = (row['Longitude'], row['Latitude'])

# Define colors for each line
unique_lines = data['Line'].unique()
line_colors = plt.cm.tab10.colors[:len(unique_lines)]  # Using a colormap to automatically assign colors

# Create a graph
G = nx.Graph()

# Add edges and distances
for _, row in data.iterrows():
    G.add_edge(row['Station from (A)'], row['Station to (B)'], weight=row['Distance (Kms)'], line=row['Line'])
    
# Use station coordinates for node positions, with a default position for missing nodes
default_position = (0, 0)  
pos = {node: station_coordinates.get(node, default_position) for node in G.nodes()}

# Print graph information
print("Graph nodes:", G.nodes())
print("Graph edges:", G.edges(data=True))
print()


# Draw the graph with edges colored by line
plt.figure(figsize=(12, 8))

for i, line in enumerate(unique_lines):
    line_data = data[data['Line'] == line]
    edges = [(row['Station from (A)'], row['Station to (B)']) for _, row in line_data.iterrows()]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=line_colors[i], width=2, label=f'{line} Line')

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='lightblue')

# Draw node labels with adjusted alignments
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontsize=5, ha='center', va='center', fontweight='bold')

# Draw the edge labels
edge_labels = {(row['Station from (A)'], row['Station to (B)']): row['Distance (Kms)'] for _, row in data.iterrows()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black')

# Add legend and title
plt.legend(scatterpoints=1, loc='lower right', ncol=1, fontsize=10)
plt.title('London Underground Network')

# Display plot
plt.show()

# Calculate total length of the transport network
total_length = sum(data['Distance (Kms)'])

# Calculate average distance between the stations
average_distance = total_length / len(data)

# Calculate standard deviation of the distances between the stations
distances_list = data['Distance (Kms)'].tolist()
standard_deviation = np.std(distances_list)

# Print the results
print("Total length of the transport network:", total_length)
print("Average distance between the stations:", average_distance)
print("Standard deviation of the distances between the stations:", standard_deviation)
