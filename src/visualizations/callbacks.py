# This file defines and registers all callback function
from datetime import datetime
import json
from dash.dependencies import Input, Output, State, ALL
# from tkinter import ALL
from dash import dcc, html

import dash
from matplotlib import figure
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from telemetry import get_location_data, get_car_data, get_lap_data

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
        "location": get_location_data(9165, 55, "2023-09-17T12:00:00+00:00", "2023-09-18"),
        "car": get_car_data(9165, 55, "2023-09-17T12:00:00+00:00", "2023-09-18"),
        "lap": get_lap_data(9165, 55)
    },
    "Driver 4": {
        "location": get_location_data(9165, 4, "2023-09-17T12:00:00+00:00", "2023-09-18"),
        "car": get_car_data(9165, 4,"2023-09-17T12:00:00+00:00", "2023-09-18"),
        "lap": get_lap_data(9165, 4)
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

    return x_coords, y_coords
    # # Convert each point to geospatial coordinates
    # latitudes = []
    # longitudes = []
    # for x, y in zip(x_coords, y_coords):
    #     latitude, longitude = cartesian_to_geospatial(x, y)
    #     latitudes.append(latitude)
    #     longitudes.append(longitude)

    # return latitudes, longitudes

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
            Output("brake-display", "value"),
            Output("rpm-display", "value"),
            Output("lap-number-display", "value"),
            Output("time-stamp-display", "value"),
            Output("leaderboard-content", "children"),
            Output("saved-zoom", "data"),  # Store zoom state in a dcc.Store
        ],  
        # Output for speed display
        [
            Input('interval-component', 'n_intervals'),
            Input("selected-driver", "data"),
            Input("circuit-map", "relayoutData"),  # Capture user zoom/pan changes
        ],
        State("saved-zoom", "data"),  # Retrieve the saved zoom state
    )
    def update_driver_position(n_intervals, selected_driver, relayout_data, saved_zoom):
        # Default to Driver 55 if no driver is selected
        if selected_driver not in telemetry_data:
            print(f"Invalid driver selected: {selected_driver}")
        
        # Handle zoom/pan persistence
        if relayout_data:
        # Update saved zoom state if the user interacts with the map
            saved_zoom = {
                "xaxis.range[0]": relayout_data.get("xaxis.range[0]"),
                "xaxis.range[1]": relayout_data.get("xaxis.range[1]"),
                "yaxis.range[0]": relayout_data.get("yaxis.range[0]"),
                "yaxis.range[1]": relayout_data.get("yaxis.range[1]"),
        }

        # Fetch telemetry data for the selected driver
        location_data = telemetry_data[selected_driver]["location"]
        car_data = telemetry_data[selected_driver]["car"]
        lap_data = telemetry_data[selected_driver]["lap"]

        

        # Extract data for visualization
        x_coords = [point["x"] for point in location_data]
        y_coords = [point["y"] for point in location_data]
        time_stamps = [point["date"] for point in location_data]
        lap_time_stamps = [point["date_start"] for point in lap_data]

        # time_stamps = lap_time_stamps

        
       # Get the current timestamp
        time_index = 0 + n_intervals % len(time_stamps)
        lap_time_index = n_intervals % len(time_stamps)

        time_index_55 = 15000 + n_intervals % len(x_coords_55)
        time_index_4 = 15000 + n_intervals % len(x_coords_4)
        current_timestamp = time_stamps[time_index]

        print("time_index = ", time_index)
        print("time_index_55 = ", time_index_55)
        print("time_index_4 = ", time_index_4)
        print("current_timestamp = ", time_stamps[time_index])
        print("lap_current_timestamp = ", lap_time_stamps)
        
        # Ensure all elements in `lap_time_stamps` are strings and valid ISO format timestamps
        valid_lap_time_stamps = [
            ts for ts in lap_time_stamps if isinstance(ts, str)
        ]

        # Convert timestamps to datetime objects
        try:
            lap_current_timestamps_dt = [
                datetime.fromisoformat(ts) for ts in valid_lap_time_stamps
            ]
            current_timestamp_dt = datetime.fromisoformat(current_timestamp)
        except ValueError as e:
            print("Error parsing timestamp:", e)
            raise

        # # Convert timestamps to datetime objects for comparison
        # current_timestamp_dt = datetime.fromisoformat(current_timestamp)
        # lap_current_timestamps_dt = [datetime.fromisoformat(ts) for ts in valid_lap_time_stamps]

        # Determine the current lap
        current_lap = 0  # Default if no laps match
        for i, lap_start in enumerate(lap_current_timestamps_dt):
            if lap_start <= current_timestamp_dt:
                current_lap = i + 1  # Laps are 1-indexed
            else:
                break  # Exit loop once we've passed the current timestamp

        # Output the result
        print(f"The driver is currently on lap {current_lap}.")

        closest_data = min(
            car_data,
            key=lambda point: abs((datetime.fromisoformat(point["date"]).timestamp() - datetime.fromisoformat(current_timestamp).timestamp()))
        )
        speed = closest_data["speed"]  # Safely extract speed
        throttle = closest_data["throttle"]
        brake = closest_data["brake"]
        rpm = closest_data["rpm"]
        driver_number = closest_data["driver_number"]

        next_time_index = (time_index + 1) % len(x_coords)

        # Compute a fraction of the way between the current position and the next
        fraction = (n_intervals % 10) / 10  # Smooth transition over 10 intervals (100 ms each)

        x_position = x_coords[time_index] + fraction * (x_coords[next_time_index] - x_coords[time_index])
        y_position = y_coords[time_index] + fraction * (y_coords[next_time_index] - y_coords[time_index])

        # Print current positions for debugging
        print(f"Selected driver - #: {driver_number}, lat: {x_coords_55[time_index]}, lon: {y_coords_55[time_index]}, speed_55: {speed}, throttle_55: {throttle}, brake_55: {brake}, rpm_55: {rpm}, lap #: {current_lap}")
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
                # go.Scattermapbox(
                # lat=x_coords_55,  # Example latitude of a driver (replace with actual)
                # lon=y_coords_55,  # Example longitude (replace with actual)
                # mode="markers",
                # marker=dict(size=4, color="red")
                # ),
                # go.Scattermapbox(
                #     lat=x_coords_55,
                #     lon=y_coords_55,
                #     mode="lines",
                #     line=dict(width=2, color="red"),
                #     name="Track"
                # ),
                go.Scattergl(  # Use scattergl for better performance with frequent updates
                x=x_coords_55, 
                y=y_coords_55, 
                mode="lines", 
                name="Circuit",
                line=dict(color="white", width=3)
                ),
                go.Scattergl(  # Use scattergl for the other driver
                x=[x_coords_55[time_index]], 
                y=[y_coords_55[time_index]], 
                mode="markers", 
                name="Carlos Sainz",
                marker=dict(size=10, color="red")
                ),
                go.Scattergl(  # Use scattergl for the other driver
                x=[x_coords_4[time_index]], 
                y=[y_coords_4[time_index]], 
                mode="markers", 
                name="Lando Norris",
                marker=dict(size=10, color="orange")
                )
            ],
            layout=go.Layout(
                plot_bgcolor='#20242c',  # Background color of the plot area (inside the graph)
                paper_bgcolor='#20242c',  # Background color outside the graph
                xaxis=dict(
                    title=None,
                    showgrid=False,  # Hide the grid lines on the x-axis
                    zeroline=False,  # Hide the zero line
                    showticklabels=False
                ),
                yaxis=dict(
                    title=None,
                    showgrid=False,  # Hide the grid lines on the y-axis
                    zeroline=False,  # Hide the zero line
                    showticklabels=False
                ),
                font=dict(color='white'),  # Font color for axes and title
                title="Circuit Map"
            )
            # layout=go.Layout(
            #     mapbox=dict(
            #         accesstoken=MAPBOX_ACCESS_TOKEN,  # Use your Mapbox token
            #         center=dict(lat=1.2906047141616643, lon=103.8572531333833),  # Map center (update with actual circuit center)
            #         zoom=13,  # Zoom level (adjust for the circuit)
            #         style=MAPBOX_STYLE_URL  # Mapbox streets style for Google-like look
            #     ),
            #     margin={"r":0,"t":0,"l":0,"b":0},
            #     # paper_bgcolor="#20242c",
            # )
        )
        # Lap number update
        # lap_number_text = f"Lap #: {lap_number}"
            # Apply saved zoom/pan state if available
        if saved_zoom:
            updated_map.update_layout(
                xaxis_range=[saved_zoom.get("xaxis.range[0]"), saved_zoom.get("xaxis.range[1]")],
                yaxis_range=[saved_zoom.get("yaxis.range[0]"), saved_zoom.get("yaxis.range[1]")],
        )

        return updated_map, speed, throttle, brake, rpm, current_lap, current_timestamp, leaderboard_content, saved_zoom
