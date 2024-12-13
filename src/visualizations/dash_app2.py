# from dash import Dash, dcc, html
# import plotly.express as px
# import pandas as pd
# import requests
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go

# def create_dash_app(car_data):
#     app = Dash(__name__)

#     # Fetch telemetry data for both drivers
#     response_driver_55 = requests.get(f'https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159')
#     response_driver_16 = requests.get(f'https://api.openf1.org/v1/car_data?driver_number=16&session_key=9159')

#     # Fetch lap data for both drivers
#     lap_data_55 = requests.get(f'https://api.openf1.org/v1/laps?session_key=9159&driver_number=55').json()
#     lap_data_16 = requests.get(f'https://api.openf1.org/v1/laps?session_key=9159&driver_number=16').json()
    
#     # Fetch location data for both drivers
#     location_data_55 = requests.get(f'https://api.openf1.org/v1/location?session_key=9159&driver_number=55').json()
#     location_data_16 = requests.get(f'https://api.openf1.org/v1/location?session_key=9159&driver_number=16').json()
    

#     # Convert car data and location data to DataFrames
#     car_data_55 = pd.DataFrame(response_driver_55.json())
#     car_data_16 = pd.DataFrame(response_driver_16.json())

#     location_55 = pd.DataFrame(location_data_55)
#     location_16 = pd.DataFrame(location_data_16)

#     # Combine data from both drivers
#     car_data = pd.concat([car_data_55, car_data_16, location_16, location_55])

#     # Plot speed over time using plotly
#     fig = px.line(
#         car_data, 
#         x="date", 
#         y="speed",  
#         color="driver_number",
#         title="Speed over Time",
#         labels={"date": "Time", "speed": "Speed (km/h)"}
#     )

#     # Extract lap start times for both drivers
#     lap_start_times_55 = pd.to_datetime([lap['date_start'] for lap in lap_data_55], errors='coerce')
#     lap_start_times_16 = pd.to_datetime([lap['date_start'] for lap in lap_data_16], errors='coerce')

#     # Add vertical lines for each lap start time
#     for lap_start in lap_start_times_55:
#         fig.add_vline(x=lap_start, line=dict(color='red', dash='dash'))

#     for lap_start in lap_start_times_16:
#         fig.add_vline(x=lap_start, line=dict(color='blue', dash='dash'))

#     # Initial empty figure for car location on circuit
#     fig_location = go.Figure()

#     app.layout = html.Div([
#         html.H1("F1 Car Telemetry Dashboard", style={'textAlign': 'center'}),
#         dcc.Graph(id='speed-over-time', figure=fig),  # Display plot
#         dcc.Graph(id='location-on-circuit', figure=fig_location),  # Display location graph

#          # Play/Pause Button
#         html.Button('Play/Pause', id='play-button', n_clicks=0),

#         # Interval component to update positions
#         dcc.Interval(
#             id='interval-component',
#             interval=1000,  # Update every second
#             n_intervals=0
#         ),

#         dcc.Dropdown(
#             id='driver-dropdown', 
#             options=[{'label': f'Driver {x}', 'value': x} for x in car_data['driver_number'].unique()],
#             value=car_data['driver_number'].iloc[0]
#         ),
#         html.Div(id='output-container')
#     ])
    
#     @app.callback(
#         [Output('location-on-circuit', 'figure'),
#          Output('interval-component', 'disabled')],
#         [Input('play-button', 'n_clicks'),
#          Input('interval-component', 'n_intervals')]
#     )
#     def update_location(n_clicks, n_intervals):
#         # Handle play/pause logic
#         if n_clicks is None or n_clicks % 2 == 0:
#             # Plot the location when paused
#             fig_location = go.Figure(
#                 data=[
#                     go.Scatter(x=location_55['x'], y=location_55['y'], mode='markers', name='Driver 55', marker=dict(color='blue')),
#                     go.Scatter(x=location_16['x'], y=location_16['y'], mode='markers', name='Driver 16', marker=dict(color='red'))
#                 ],
#                 layout=go.Layout(
#                     title="Car Location on Circuit",
#                     xaxis=dict(title="X Coordinate"),
#                     yaxis=dict(title="Y Coordinate")
#                 )
#             )
#             return fig_location, False  # Disable interval when paused
#         else:
#             # Update location dynamically when "playing"
#             # Here you can update the positions over time (modify this logic based on your data)
#             fig_location = go.Figure(
#                 data=[
#                     go.Scatter(x=location_55['x'][:n_intervals+1], y=location_55['y'][:n_intervals+1], mode='lines+markers', name='Driver 55', marker=dict(color='blue')),
#                     go.Scatter(x=location_16['x'][:n_intervals+1], y=location_16['y'][:n_intervals+1], mode='lines+markers', name='Driver 16', marker=dict(color='red'))
#                 ],
#                 layout=go.Layout(
#                     title="Car Location on Circuit",
#                     xaxis=dict(title="X Coordinate"),
#                     yaxis=dict(title="Y Coordinate")
#                 )
#             )
#             return fig_location, True  # Enable interval when playing
        
#     return app