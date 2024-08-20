import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


stations_line = {}
def count_the_line(station, line):
    if station not in stations_line:
        stations_line[station] = set()
    stations_line[station].add(line) 
    
# Load the data from the CSV file for road distances
file_path = 'process4.csv'
print(f"Loading data from: {file_path}")
data = pd.read_csv(file_path, encoding='latin1')

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
line_colors = {
    'Bakerloo ': 'brown',
    'Central ': 'red',
    'Jubilee ': 'grey',
    'Northern ': 'black',
    'Victoria': 'lightblue',
}

# Create a graph
G = nx.Graph()

# Add edges and distances
for _, row in data.iterrows():
    G.add_edge(row['Station from (A)'], row['Station to (B)'], weight=row['Distance (Kms)'], line=row['Line'])
    count_the_line(row['Station from (A)'], row['Line'])
    count_the_line(row['Station to (B)'], row['Line'])   
    
print("Stations line:", stations_line)
# Use station coordinates for node positions, with a default position for missing nodes
default_position = (0, 0)  
pos = {node: station_coordinates.get(node, default_position) for node in G.nodes()}

# Print graph information
print("Graph nodes:", G.nodes())
print("Graph edges:", G.edges(data=True))
print()

# Draw the graph with edges colored by line
plt.figure(figsize=(18, 10))


count = 0
for i, line in enumerate(unique_lines):
    line_data = data[data['Line'] == line]
    edges = [(row['Station from (A)'], row['Station to (B)']) for _, row in line_data.iterrows()]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=line_colors[line], width=2, label=f'{line} Line')
    

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=30, node_color='white',  edgecolors='purple', linewidths=1)

for node in G.nodes():
    if node in stations_line and len(stations_line[node]) > 1:
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=30, node_color='white', edgecolors='purple', linewidths=1)
    elif node in stations_line:
        line = list(stations_line[node])[0]  # Convert the set to a list and access the first element
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_size=30, node_color=line_colors[line], edgecolors=line_colors[line], linewidths=1)
    
# Draw node labels with adjusted alignments
for node, (x, y) in pos.items():
    plt.text(x+0.001, y, node, fontsize=5, ha='left', va='baseline', fontweight='bold', rotation=20, color='black', alpha=0.7,)
            #  bbox=dict(facecolor='white', alpha=0.5))

# Draw the edge labels
edge_labels = {(row['Station from (A)'], row['Station to (B)']): row['Distance (Kms)'] for _, row in data.iterrows()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_color='black', label_pos=0.5)

# Create legend 
legend_elements = []
for line, color in line_colors.items():
    legend_elements.append(plt.Line2D([0], [0], marker='o', color=color, label=line, markerfacecolor=color, markersize=5))

legend_elements.append(plt.Line2D([], [], marker='o', color='purple', label='Interchange', markerfacecolor='w', markersize=5, linestyle='None'))

# Add legend and title
plt.legend(handles=legend_elements, scatterpoints=1, loc='lower right', ncol=1, fontsize=7)
plt.title('London Underground Network', fontsize=15)

# Display plot
plt.show()