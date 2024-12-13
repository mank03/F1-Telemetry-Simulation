import dash
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import time
import plotly.graph_objs as go
import requests

def fetch_telemetry_data(session_key, driver_number):
    url = f"https://api.openf1.org/v1/location?session_key={session_key}&driver_number={driver_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the list of telemetry points
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

telemetry_driver_55 = fetch_telemetry_data(9159, 55)

# Extracting time (in seconds), x, and y for visualization
time_stamps_55 = [point["date"] for point in telemetry_driver_55]
x_coords_55 = [point["x"] for point in telemetry_driver_55]
y_coords_55 = [point["y"] for point in telemetry_driver_55]

telemetry_driver_4 = fetch_telemetry_data(9159, 4)

x_coords_4 = [point["x"] for point in telemetry_driver_4]
y_coords_4 = [point["y"] for point in telemetry_driver_4]

# # Convert time stamps to a relative timeline for the slider
# import datetime

# base_time = datetime.datetime.fromisoformat(telemetry_driver_55[0]["date"])
# time_seconds = [
#     (datetime.datetime.fromisoformat(point["date"]) - base_time).total_seconds()
#     for point in telemetry_driver_55
# ]

# Layout of the circuit
circuit_map = go.Figure(
    data=[go.Scatter(x=x_coords_55, y=y_coords_55, mode="lines", name="Circuit", line=dict(color="blue", width=2))]
)

app = dash.Dash(__name__)

# Set up the initial state for the time
time_index_55 = 15000  # Start from the first position

app.layout = html.Div([
    dcc.Graph(id="circuit-map", figure=circuit_map),
    dcc.Interval(
        id='interval-component',
        interval=100,  # Time interval in milliseconds (1000 ms = 1 second)
        n_intervals=0
    )
    # dcc.Slider(
    #     id="time-slider",
    #     min=min(time_seconds),
    #     max=max(time_seconds),
    #     step=0.1,
    #     value=min(time_seconds),
    #     marks={int(t): str(int(t)) for t in time_seconds},  # Display seconds on slider
    # ),
])

@app.callback(
    dash.dependencies.Output("circuit-map", "figure"),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_driver_position(n_intervals):
    # Calculate the index for the current position of the driver
    time_index_55 = 15000 + n_intervals % len(x_coords_55)
    time_index_4 = 15000 + n_intervals % len(x_coords_4)

    print('time index of driver 55 = ',time_index_55)

    # Print the current driver's position (x, y)
    print(f"Driver's current position - x: {x_coords_55[time_index_55]}, y: {y_coords_55[time_index_55]}")

    # Find the closest time in telemetry data
    # closest_index = min(
    #     range(len(time_seconds)),
    #     key=lambda i: abs(time_seconds[i] - selected_time)
    # )
    # x_pos, y_pos = x_coords[closest_index], y_coords[closest_index]

    # Update driver position on the circuit map
    updated_map = go.Figure(data=[
        go.Scatter(
            x=x_coords_55, 
            y=y_coords_55, 
            mode="lines", 
            name="Circuit"
        ),
        go.Scatter(
            x=[x_coords_55[time_index_55]], 
            y=[y_coords_55[time_index_55]], 
            mode="markers", 
            name="Carlos Sainz",
            marker=dict(size=10, color="red")
        ),
        go.Scatter(
            x=[x_coords_4[time_index_4]], 
            y=[y_coords_4[time_index_4]], 
            mode="markers", 
            name="Lando Norris",
            marker=dict(size=10, color="orange")
        )
    ])
    return updated_map


if __name__ == "__main__":
    app.run_server(debug=True)
