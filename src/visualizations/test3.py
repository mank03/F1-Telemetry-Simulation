# This file defines and registers all callback function
from datetime import datetime
import json
from dash.dependencies import Input, Output, State, ALL
# from tkinter import ALL
from dash import dcc, html

import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from telemetry import get_location_data, get_car_data

# Mapbox access token (replace with your token)
MAPBOX_STYLE_URL = "mapbox://styles/mkonnur/cm4omuz6e008m01s8446k9r6n"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWtvbm51ciIsImEiOiJjbTRvaWNmankwazByMm1xNG5teHF6dG54In0.jCPJgwqG3medIN6WRrY9XA"

LAT_REF = 1.29148788242174
LON_REF = 103.85494601254759
X_REF = -9465
Y_REF = 540
LAT_SCALE = 2.933e-6  # Calculated earlier
LON_SCALE = 8.835e-7  # Calculated earlier



# Load GeoJSON data from file
with open("singapore.geojson", "r") as file:
    geojson_data = json.load(file)

# Extract line coordinates from GeoJSON
line_coordinates = geojson_data["features"][0]["geometry"]["coordinates"]
line_lons, line_lats = zip(*line_coordinates)

# Fetch telemetry data
telemetry_data = {
    "Driver 55": {
        "location": get_location_data(9159, 55),
        "car": get_car_data(9159, 55)
    },
    "Driver 4": {
        "location": get_location_data(9159, 4),
        "car": get_car_data(9159, 4)
    }
}

# Function to convert Cartesian coordinates to geospatial
def cartesian_to_geospatial(x, y):
    """
    Converts Cartesian coordinates (x, y) to geospatial coordinates (latitude, longitude).
    """
    # Compute deltas
    delta_x = x - X_REF
    delta_y = y - Y_REF

    # Convert to geospatial
    latitude = LAT_REF + delta_x * LAT_SCALE
    longitude = LON_REF + delta_y * LON_SCALE

    return latitude, longitude


# Helper function to extract x and y coordinates
def get_driver_coordinates(driver_number, telemetry_data):
    location_data = telemetry_data[driver_number]["location"]
    x_coords = [point["x"] for point in location_data]
    y_coords = [point["y"] for point in location_data]

    # # Convert each point to geospatial coordinates
    # latitudes = []
    # longitudes = []
    # for x, y in zip(x_coords, y_coords):
    #     latitude, longitude = cartesian_to_geospatial(x, y)
    #     latitudes.append(latitude)
    #     longitudes.append(longitude)
    return x_coords, y_coords

# Extract coordinates for each driver using the helper function
x_coords_4, y_coords_4   = get_driver_coordinates("Driver 4", telemetry_data)
x_coords_55, y_coords_55   = get_driver_coordinates("Driver 55", telemetry_data)

# # Extract data for visualization
# x_coords_55 = [point["x"] for point in telemetry_driver_55]
# y_coords_55 = [point["y"] for point in telemetry_driver_55]

# # Fetch the latest speed data for driver 55
# car_data_55 = get_car_data(9159, 55)
# speed_55 = [point["speed"] for point in car_data_55]  # speed of driver 55
# throttle_55 = [point["throttle"] for point in car_data_55]  # speed of driver 55
# rpm_55 = [point["rpm"] for point in car_data_55]  # speed of driver 55
# time_stamps_55 = [point["date"] for point in telemetry_driver_55]  # ISO-format timestamps


def register_callbacks(app):
    @app.callback(
        Output("selected-driver", "data"),
        [Input({"type": "leaderboard-item", "index": ALL}, "n_clicks")],
        State("selected-driver", "data"),
        prevent_initial_call=True
    )
    def select_driver(n_clicks, current_selection):
        ctx = dash.callback_context
        print("n_clicks = ", n_clicks)
        # This ensures that we only process the click when the leaderboard button is clicked
        if ctx.triggered and not any(n_clicks_value > 0 for n_clicks_value in n_clicks):
            # This means no leaderboard button was clicked, so we keep the current selection
            print("1. current selection (not clicked):", current_selection)
            return current_selection
        print("2. current selection:", current_selection)
        # Extract the clicked component's ID
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        triggered_id_dict = eval(triggered_id)  # Convert string to dictionary
        index = triggered_id_dict.get("index")  # Get the index
        print("Clicked Driver ID:", index)
        # Map the index to the driver name (match `leaderboard_data` to `telemetry_data`)
        leaderboard_data = ["Driver 55", "Driver 4", "Driver 16"]  # Ordered list of drivers
        return leaderboard_data[index] if index is not None else current_selection
        
    @app.callback(
        [
            Output("circuit-map", "figure"),
            Output("speed-display", "value"),
            Output("throttle-display", "value"),
            Output("rpm-display", "value"),
            Output("leaderboard-content", "children")
        ],  
        # Output for speed display
        [
            Input('interval-component', 'n_intervals'),
            Input("selected-driver", "data")
        ]
    )
    def update_driver_position(n_intervals, selected_driver):
        # Default to Driver 55 if no driver is selected
        if selected_driver not in telemetry_data:
            print(f"Invalid driver selected: {selected_driver}")
        
        # Fetch telemetry data for the selected driver
        location_data = telemetry_data[selected_driver]["location"]
        car_data = telemetry_data[selected_driver]["car"]



        # Extract data for visualization
        x_coords = [point["x"] for point in location_data]
        y_coords = [point["y"] for point in location_data]
        time_stamps = [point["date"] for point in location_data]
        
       # Get the current timestamp
        time_index = 15000 + n_intervals % len(time_stamps)
        time_index_55 = 15000 + n_intervals % len(x_coords_55)
        time_index_4 = 15000 + n_intervals % len(x_coords_4)
        current_timestamp = time_stamps[time_index]

        print("current_timestamp = ", time_stamps[time_index])


        closest_data = min(
            car_data,
            key=lambda point: abs((datetime.fromisoformat(point["date"]).timestamp() - datetime.fromisoformat(current_timestamp).timestamp()))
        )
        speed = closest_data["speed"]  # Safely extract speed
        throttle = closest_data["throttle"]
        rpm = closest_data["rpm"]
        driver_number = closest_data["driver_number"]

        
        next_time_index = (time_index + 1) % len(x_coords)

        # Compute a fraction of the way between the current position and the next
        fraction = (n_intervals % 10) / 10  # Smooth transition over 10 intervals (100 ms each)

        x_position = x_coords[time_index] + fraction * (x_coords[next_time_index] - x_coords[time_index])
        y_position = y_coords[time_index] + fraction * (y_coords[next_time_index] - y_coords[time_index])
        
        lat_55, lon_55 = cartesian_to_geospatial(x_coords_55[time_index_55], y_coords_55[time_index_55])
        lat_path, lon_path = zip(*[cartesian_to_geospatial(x, y) for x, y in zip(x_coords_55, y_coords_55)])


        # Print current positions for debugging
        print(f"Selected driver - #: {driver_number}, lat: {lat_55}, x: {x_coords_55[time_index]}, lon: {lon_55}, y: {y_coords_55[time_index]}, speed_55: {speed}, throttle_55: {throttle}, rpm_55: {rpm}")
        # print(f"Driver 4 - x: {x_coords[time_index]}, y: {y_coords[time_index]}")
        # Example leaderboard data (replace with actual data source)
        
        # Leaderboard content
        leaderboard_data = [
            {"name": "Driver 55", "time": "1:23.456", "id": "Driver 55"},
            {"name": "Driver 4", "time": "1:24.123", "id": "Driver 4"},
            {"name": "Driver 16", "time": "1:24.789", "id": "Driver 16"},
        ]
        leaderboard_content = [
            html.Div(
                children=[
                    html.Span(f"{i + 1}. {entry['name']}", style={'fontWeight': 'bold'}),
                    html.Span(f" - {entry['time']}", style={'marginLeft': '10px'})
                ],
                style={'marginBottom': '10px', 'cursor': 'pointer'},
                id={"type": "leaderboard-item", "index": i},  # Use dictionary format for the id
                n_clicks = 0
            )
            for i, entry in enumerate(leaderboard_data)
        ]



        # Here you can update the map with actual data and driver positions
        updated_map = go.Figure(
            data=[
                # Add the line showing the driver's path
                go.Scattermapbox(
                    lat=[x_coords_55[time_index_55]],  # Latitude for the path
                    lon=[y_coords_55[time_index_55]],  # Longitude for the path
                    mode="lines",  # Only lines for the path
                    name="Driver 55 Path",
                    line=dict(width=3, color="blue"),  # Customize line style
                ),
                go.Scattermapbox(
                    lat=[lat_55],  # Example latitude of a driver (replace with actual)
                    lon=[lon_55],  # Example longitude (replace with actual)
                    mode="markers",
                    name="Carlos Sainz",
                    marker=dict(size=10, color="red"),
                ),
                # go.Scattermapbox(
                #     lat=line_lats,
                #     lon=line_lons,
                #     mode="lines",
                #     line=dict(width=2, color="red"),
                #     name="Track"
                # ),
                # go.Scattergl(  # Use scattergl for better performance with frequent updates
                # y=x_coords_55, 
                # x=y_coords_55, 
                # mode="lines", 
                # name="Circuit",
                # line=dict(color="blue", width=2)
                # ),
                # go.Scattergl(  # Use scattergl for the other driver
                # x=[x_coords_4[time_index_4]], 
                # y=[y_coords_4[time_index_4]], 
                # mode="markers", 
                # name="Lando Norris",
                # marker=dict(size=10, color="orange")
                # ),
                # go.Scattergl(  # Use scattergl for the other driver
                # y=[x_coords_55[time_index_55]], 
                # x=[y_coords_55[time_index_55]], 
                # mode="markers", 
                # name="Carlos Sainz",
                # marker=dict(size=10, color="red")
                # )
            ],
            layout=go.Layout(
                mapbox=dict(
                    accesstoken=MAPBOX_ACCESS_TOKEN,  # Use your Mapbox token
                    center=dict(lat=1.2906047141616643, lon=103.8572531333833),  # Map center (update with actual circuit center)
                    zoom=12,  # Zoom level (adjust for the circuit)
                    style=MAPBOX_STYLE_URL  # Mapbox streets style for Google-like look
                ),
                margin={"r":0,"t":0,"l":0,"b":0},
                # paper_bgcolor="#20242c",
            )
        )
        return updated_map, speed, throttle, rpm, leaderboard_content
