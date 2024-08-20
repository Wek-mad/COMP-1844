import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the CSV File
stations_data = pd.read_csv('stations.csv')

# Step 2: 
# Filter the data
stations_data = stations_data[stations_data['Zone'] == '1']

# Drop NA values
stations_data.dropna(inplace=True)

# Step 3: Convert Coordinates
# Latitude and Longitude are already in the correct format for plotting

# Step 4: Visualize Data on a Map
plt.figure(figsize=(12, 10))

# Plot stations as points
plt.scatter(stations_data['Longitude'], stations_data['Latitude'], c='blue', marker='o', s=10, label='Stations')

# Step 5: Add Annotations
for index, row in stations_data.iterrows():
    plt.text(row['Longitude'], row['Latitude'], row['Station'], fontsize=8, ha='right')

plt.title('London Underground Stations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.legend()
plt.show()
