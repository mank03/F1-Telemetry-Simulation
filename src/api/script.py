from urllib.request import urlopen
import json
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualizations.matplotlib_visuals import plot_speed_vs_gear
from visualizations.matplotlib_visuals import plot_throttle_over_time

from visualizations.dash_app import create_dash_app


# The main entry point for the script
if __name__ == "__main__":
    # Fetch data from the API
    response = urlopen('https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159')
    data = json.loads(response.read().decode('utf-8'))
    car_data = pd.DataFrame(data)

    # Check if the dataset is not empty
    if not car_data.empty:
        # print("Displaying Matplotlib Visualization...")
        # plot_throttle_over_time(car_data)
        # plot_speed_vs_gear(car_data)
        
        print("Starting Dash Application...")
        create_dash_app(car_data).run_server(debug=True)
    else:
        print("No data available for visualization.")