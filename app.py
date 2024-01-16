import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import os

def calculate_net_area_between_scatter_plots(folder_name):
    # Define the CSV file name
    csv_file = "transects.csv"

    # Construct the full file path
    file_path = os.path.join(folder_name, csv_file)

    # Read the CSV file, allowing missing values
    df = pd.read_csv(file_path)

    # Drop rows where either x1 or x2 is missing
    df = df.dropna(subset=['x1', 'x2'])

    # Extract x and y values for both scatter plots, handling missing values
    x1, y1 = df['x1'].dropna(), df['y1'].dropna()
    x2, y2 = df['x2'].dropna(), df['y2'].dropna()

    # Create interpolation functions for both sets of y-values
    interp_y1 = interp1d(x1, y1, bounds_error=False, fill_value="extrapolate")
    interp_y2 = interp1d(x2, y2, bounds_error=False, fill_value="extrapolate")

    # Find the overlap in x values
    x_overlap = np.sort(np.unique(np.concatenate((x1[x1.between(x2.min(), x2.max())], x2[x2.between(x1.min(), x1.max())]))))

    # Calculate interpolated y-values
    interp_y1_vals = interp_y1(x_overlap)
    interp_y2_vals = interp_y2(x_overlap)

    # Calculate the difference in y-values
    y_diff = interp_y2_vals - interp_y1_vals

    # Calculate the net area between the two curves
    net_area = np.trapz(y_diff, x_overlap)

    return net_area

def custom_sort(folder):
    # Sort by number first, then by 'pre' or 'post'
    number, period = folder.split('-')
    return (int(number[1:]), period == 'post')  # 'pre' will come before 'post'

if __name__ == "__main__":
    base_dir = '.'  # Replace with your base directory path
    output_file = "net-areas.txt"  # Output file for net areas

    # Get a list of all directories that start with 'T'
    folders = [item for item in os.listdir(base_dir) if os.path.isdir(item) and item.startswith('T')]

    # Sort the list of directories using the custom sorting function
    folders.sort(key=custom_sort)

    with open(output_file, 'w') as f:
        for folder in folders:
            folder_path = os.path.join(base_dir, folder)
            area = calculate_net_area_between_scatter_plots(folder_path)
            folder_name = folder.replace('./', '')  # Remove './' from folder name
            f.write(f"Net loss / accumulation of sediment for {folder_name}: {area} square feet\n")