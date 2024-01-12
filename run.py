import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from obj_raycasting import raycasting
from coord_to_index import to_index
from map_to_xlsx import to_xlsx

# Range: raycast from -n to +n coordinates in xyz-axis
# Scale: number of points in a single coordinate unit(1)
data, scale = raycasting()

# Create a Tkinter root widget
root = tk.Tk()
root.withdraw()  # Hide the main window

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Open a file dialog to choose file path and name
file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                        filetypes=[('CSV files', '*.csv')],
                                        title='Save coordinates file as',
                                        initialfile='output_coord',
                                        initialdir=script_directory)

# Check if a file path was provided
if file_path:
    # Write DataFrame to the chosen file
    data.to_csv(file_path, index=False, header=False)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotting
ax.scatter(data['X'], data['Y'], data['Z'])

# Setting labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Show plot
plt.show()

# Convert and save to index
merged_df, nx, ny = to_index(data, scale)

# Build map and save
to_xlsx(merged_df, nx, ny)