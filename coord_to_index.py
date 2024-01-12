import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

def to_index(data, scale):
    # Reading the data
    data = data.reset_index(drop=True)
    X = data.iloc[:, 0].values
    Y = data.iloc[:, 1].values
    Z = data.iloc[:, 2].values

    # Calculating the number of cells in each direction
    nx = int(round(scale * (np.max(X) - np.min(X)))) + 1  # Ensure nx is an integer
    ny = int(round(scale * (np.max(Y) - np.min(Y)))) + 1  # Ensure ny is an integer
    nz = int(round(scale * (np.max(Z) - np.min(Z)))) + 1  # Ensure nz is an integer

    def coord_to_index(x, y, z):
        ix = (x - np.min(X)) * scale + 1
        iy = (y - np.min(Y)) * scale + 1
        iz = (np.max(Z) - z) * scale + 1  # 역순으로 변경
        i = (iz-1) * (nx * ny) + (iy-1) * nx + (ix-1) + 1
        return round(i)

    # 좌표 인덱스화
    data['I'] = data.apply(lambda row: coord_to_index(row['X'], row['Y'], row['Z']), axis=1)
    data['P'] = 1
    data = data[['I', 'P']]
    data = data.sort_values(by='I', ascending=True, ignore_index=True)

    df = pd.DataFrame({'I': range(1, nx*ny*nz+1)})
    merged_df = pd.merge(data, df, on='I', how='outer')
    merged_df = merged_df.fillna(0)
    merged_df['P'] = merged_df['P'].astype(int)
    merged_df = merged_df.sort_values(by='I', ascending=True, ignore_index=True)
    merged_df = merged_df.drop_duplicates(keep="first")
    print(merged_df)

    print("Grid size (x, y, z, xyz) :", nx, ny, nz, nx*ny*nz)
    print("Make sure to delete column title row")
    
    # Create a Tkinter root widget
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Get the script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Open a file dialog to choose file path and name
    file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                            filetypes=[('CSV files', '*.csv')],
                                            title='Save index coordinates file as',
                                            initialfile='output_index_coord',
                                            initialdir=script_directory)

    # Check if a file path was provided
    if file_path:
        # Write DataFrame to the chosen file
        merged_df.to_csv(file_path, index=False, header=False)

    # Destroy the root widget
    root.destroy()
    return merged_df, nx, ny