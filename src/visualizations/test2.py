# This file defines and registers all callback function
from datetime import datetime
from dash import dcc, html

import plotly.graph_objs as go
from dash.dependencies import Input, Output
from telemetry import get_location_data, get_car_data
# Fetch telemetry data
telemetry_driver_55 = get_location_data(9159, 55)
telemetry_driver_4 = get_location_data(9159, 4)

# Extract data for visualization
x_coords_55 = [point["x"] for point in telemetry_driver_55]
y_coords_55 = [point["y"] for point in telemetry_driver_55]

x_coords_4 = [point["x"] for point in telemetry_driver_4]
y_coords_4 = [point["y"] for point in telemetry_driver_4]


# Fetch the latest speed data for driver 55
car_data_55 = get_car_data(9159, 55)
speed_55 = [point["speed"] for point in car_data_55]  # speed of driver 55
throttle_55 = [point["throttle"] for point in car_data_55]  # speed of driver 55
rpm_55 = [point["rpm"] for point in car_data_55]  # speed of driver 55
time_stamps_55 = [point["date"] for point in telemetry_driver_55]  # ISO-format timestamps

def register_callbacks(app):
    @app.callback(
        [Output("circuit-map", "figure"),
        Output("speed-display", "value"),
        Output("throttle-display", "value"),
        Output("rpm-display", "value"),
        Output("leaderboard-content", "children")],  # Output for speed display
        [Input('interval-component', 'n_intervals')]
    )
    def update_driver_position(n_intervals):
        # Example leaderboard data (replace with actual data source)
        leaderboard_data = [
            {"name": "Driver 55", "time": "1:23.456"},
            {"name": "Driver 4", "time": "1:24.123"},
            {"name": "Driver 16", "time": "1:24.789"},
        ]
        leaderboard_content = [
            html.Div(
                style={'marginBottom': '10px'},
                children=[
                    html.Span(f"{i+1}. {entry['name']}", style={'fontWeight': 'bold'}),
                    html.Span(f" - {entry['time']}", style={'marginLeft': '10px'})
                ]
            )
            for i, entry in enumerate(leaderboard_data)
        ]
        
        time_index_55 = 15000 + n_intervals % len(x_coords_55)
        time_index_4 = 15000 + n_intervals % len(x_coords_4)

        # Fetch the timestamp corresponding to the current time_index
        current_timestamp_55 = time_stamps_55[time_index_55]
        print("current_timestamp_55 = ", current_timestamp_55)

        # Ensure car_data_55 is a list and not empty
        if isinstance(car_data_55, list) and len(car_data_55) > 0:
            # Find the closest match for the timestamp in car_data_55
            closest_data = min(
                car_data_55,
                key=lambda point: abs((datetime.fromisoformat(point["date"]).timestamp() - datetime.fromisoformat(current_timestamp_55).timestamp()))
            )
            speed_55 = closest_data["speed"]  # Safely extract speed
            throttle_55 = closest_data["throttle"]
            rpm_55 = closest_data["rpm"]
        else:
            speed_55 = 0  # Default to 0 if data is unavailable
            throttle_55 = 0
            rpm_55 = 0
        
         # Interpolate the position smoothly between the current and next point
        next_time_index_55 = (time_index_55 + 1) % len(x_coords_55)

        # Compute a fraction of the way between the current position and the next
        fraction = (n_intervals % 10) / 10  # Smooth transition over 10 intervals (100 ms each)
        
        # Linear interpolation of position (smooth movement)
        x_position = x_coords_55[time_index_55] + fraction * (x_coords_55[next_time_index_55] - x_coords_55[time_index_55])
        y_position = y_coords_55[time_index_55] + fraction * (y_coords_55[next_time_index_55] - y_coords_55[time_index_55])

        # Print current positions for debugging
        print(f"Driver 55 - x: {x_coords_55[time_index_55]}, y: {y_coords_55[time_index_55]}, speed_55: {speed_55}, throttle_55: {throttle_55}, rpm_55: {rpm_55}")
        print(f"Driver 4 - x: {x_coords_4[time_index_4]}, y: {y_coords_4[time_index_4]}")

        updated_map = go.Figure(data=[
            go.Scattergl(  # Use scattergl for better performance with frequent updates
                x=x_coords_55, 
                y=y_coords_55, 
                mode="lines", 
                name="Circuit",
                line=dict(color="blue", width=2)
            ),
            go.Scattergl(  # Use scattergl for the driver marker
                x=[x_position], 
                y=[y_position], 
                mode="markers", 
                name="Driver 55",
                marker=dict(size=10, color="red")
            ),
            go.Scattergl(  # Use scattergl for the other driver
                x=[x_coords_4[time_index_4]], 
                y=[y_coords_4[time_index_4]], 
                mode="markers", 
                name="Driver 4",
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
        return updated_map, speed_55, throttle_55, rpm_55, leaderboard_content
    





    def select_driver(n_clicks, current_selection):
        ctx = dash.callback_context
        print("Callback Context:", ctx)
        if not ctx.triggered:
            return current_selection

        # Extract the clicked component's ID
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        triggered_id_dict = eval(triggered_id)  # Convert string to dictionary
        index = triggered_id_dict.get("index")  # Get the index
        print("Clicked Driver ID:", index)
        # Map the index to the driver name (match `leaderboard_data` to `telemetry_data`)
        leaderboard_data = ["Driver 4", "Driver 55", "Driver 16"]  # Ordered list of drivers
        return leaderboard_data[index] if index is not None else current_selection