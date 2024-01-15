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

    # Combine x values and sort them
    combined_x = np.sort(np.unique(np.concatenate((x1, x2))))

    # Calculate interpolated y-values
    interp_y1_vals = interp_y1(combined_x)
    interp_y2_vals = interp_y2(combined_x)

    # Calculate the difference in y-values
    y_diff = interp_y2_vals - interp_y1_vals

    # Calculate the net area between the two curves
    net_area = np.trapz(y_diff, combined_x)

    # Write the net area to a file
    output_file = os.path.join(folder_name, "net-area.txt")
    with open(output_file, 'w') as f:
        f.write(str(net_area) + " square feet")

    return net_area

# Example usage
# folder = 'path_to_folder'
# area = calculate_net_area_between_scatter_plots(folder)
# print("Net area between scatter plots:", area)


if __name__ == "__main__":
    folder = './T1-pre'  # Replace with your folder path
    area = calculate_net_area_between_scatter_plots(folder)
    print("Net area between scatter plots:", area)