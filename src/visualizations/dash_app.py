from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import requests


def create_dash_app(car_data):
    app = Dash(__name__)

    # Fetch telemetry data for both drivers
    response_driver_55 = requests.get(f'https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159')
    response_driver_16 = requests.get(f'https://api.openf1.org/v1/car_data?driver_number=16&session_key=9159')

    # Fetch lap data for both drivers
    lap_data_55 = requests.get(f'https://api.openf1.org/v1/laps?session_key=9159&driver_number=55').json()
    lap_data_16 = requests.get(f'https://api.openf1.org/v1/laps?session_key=9159&driver_number=16').json()
    
    # Fetch location data for both drivers
    location_data_55 = requests.get(f'https://api.openf1.org/v1/location?session_key=9159&driver_number=55').json()
    location_data_16 = requests.get(f'https://api.openf1.org/v1/location?session_key=9159&driver_number=16').json()

    # Combine data from both drivers
    car_data_55 = pd.DataFrame(response_driver_55.json())
    car_data_16 = pd.DataFrame(response_driver_16.json())

    # Convert location data to DataFrames
    location_55 = pd.DataFrame(location_data_55)
    location_16 = pd.DataFrame(location_data_16)


    car_data = pd.concat([car_data_55, car_data_16, location_16, location_55])


    # Extract lap start times for both drivers
    lap_start_times_55 = pd.to_datetime([lap['date_start'] for lap in lap_data_55], errors='coerce')
    lap_start_times_16 = pd.to_datetime([lap['date_start'] for lap in lap_data_16], errors='coerce')



    # Plot speed over time using plotly
    fig = px.line(
        car_data, 
        x="date", 
        y="speed",  
        color="driver_number",
        title="Speed over Time",
        labels={"date": "Time", "speed": "Speed (km/h)"}
    )

    # Add vertical lines for each lap start time
    for lap_start in lap_start_times_55:
        fig.add_vline(x=lap_start, line=dict(color='red', dash='dash'))

    for lap_start in lap_start_times_16:
        fig.add_vline(x=lap_start, line=dict(color='blue', dash='dash'))

    # Plot car locations on the circuit
    fig_location = px.scatter(
        x=pd.concat([location_55['x'], location_16['x']]),
        y=pd.concat([location_55['y'], location_16['y']]),
        color=pd.concat([location_55['driver_number'], location_16['driver_number']]),
        title="Car Location on Circuit",
        labels={"x": "X Coordinate", "y": "Y Coordinate"},
        color_discrete_map={55: 'blue', 16: 'red'}
    )

    app.layout = html.Div([
        html.H1("F1 Car Telemetry Dashboard", style={'textAlign': 'center'}),
        dcc.Graph(id='speed-over-time', figure=fig),  # Display plot
        dcc.Graph(id='location-on-circuit', figure=fig_location),  # Display location graph

        dcc.Dropdown(
            id='driver-dropdown', 
            options=[{'label': f'Driver {x}', 'value': x} for x in car_data['driver_number'].unique()],
            value=car_data['driver_number'].iloc[0]
        ),
        html.Div(id='output-container')
    ])
    
    return app