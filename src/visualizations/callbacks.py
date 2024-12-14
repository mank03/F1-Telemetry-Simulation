# This file defines and registers all callback function
from datetime import datetime
from dash.dependencies import Input, Output, State, ALL
# from tkinter import ALL
from dash import dcc, html

import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from telemetry import get_location_data, get_car_data
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

# Helper function to extract x and y coordinates
def get_driver_coordinates(driver_number, telemetry_data):
    location_data = telemetry_data[driver_number]["location"]
    x_coords = [point["x"] for point in location_data]
    y_coords = [point["y"] for point in location_data]
    return x_coords, y_coords

# Extract coordinates for each driver using the helper function
x_coords_4, y_coords_4 = get_driver_coordinates("Driver 4", telemetry_data)
x_coords_55, y_coords_55 = get_driver_coordinates("Driver 55", telemetry_data)

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

        # Print current positions for debugging
        print(f"Selected driver - #: {driver_number}, x: {x_coords[time_index]}, y: {y_coords[time_index]}, speed_55: {speed}, throttle_55: {throttle}, rpm_55: {rpm}")
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
        updated_map = go.Figure(data=[
            go.Scattergl(  # Use scattergl for better performance with frequent updates
                x=x_coords, 
                y=y_coords, 
                mode="lines", 
                name="Circuit",
                line=dict(color="blue", width=2)
            ),
            go.Scattergl(  # Use scattergl for the driver marker
                x=[x_coords_55[time_index_55]], 
                y=[y_coords_55[time_index_55]], 
                mode="markers", 
                name="Carlos Sainz",
                marker=dict(size=10, color="red")
            ),
            go.Scattergl(  # Use scattergl for the other driver
                x=[x_coords_4[time_index_4]], 
                y=[y_coords_4[time_index_4]], 
                mode="markers", 
                name="Lando Norris",
                marker=dict(size=10, color="orange")
            )
        ], layout=go.Layout(
            plot_bgcolor='#20242c',  # Background color of the plot area (inside the graph)
            paper_bgcolor='#20242c',  # Background color outside the graph
            font=dict(color='white'),  # Font color for axes and title
            xaxis=dict(
                showgrid=False,  # Hide the grid lines on the x-axis
                zeroline=False,  # Hide the zero line
            ),
            yaxis=dict(
                showgrid=False,  # Hide the grid lines on the y-axis
                zeroline=False,  # Hide the zero line
            ),
            title="Circuit Map"
        ))
        return updated_map, speed, throttle, rpm, leaderboard_content
