import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_daq as daq
import plotly.graph_objs as go

def create_layout():
    return html.Div(  # Main container
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'backgroundColor': '#20242c',
            'height': '100vh',
            'padding': '20px',
            'color': 'white'  # Ensure text is visible on dark background
        },
        children=[
            html.Div(  # Header section
                html.H1("F1 Telemetry Simulation", style={'textAlign': 'center'}),
                style={'marginBottom': '20px'}
            ),
            html.Div(  # Main content: Leaderboard and Circuit Map
                style={
                    'display': 'flex',
                    'flexDirection': 'row',  # Arrange leaderboard and circuit map side by side
                    'gap': '20px',  # Add spacing between components
                },
                children=[
                    html.Div(  # Leaderboard container
                        id="leaderboard-container",
                        style={
                            'backgroundColor': '#white',
                            'padding': '0px',
                            'borderRadius': '5px',
                            'width': '250px',
                            'height': '600px',
                            'overflowY': 'auto'  # Allow scrolling for many drivers
                        },
                        children=[
                            html.H4("Leaderboard", style={'textAlign': 'center'}),
                            html.Div(id="leaderboard-content")  # Populated by callback
                        ]
                    ),
                    html.Div(  # Circuit map container
                        dcc.Graph(
                            id="circuit-map",
                            config={'displayModeBar': False},
                            style={'flex': '1'}
                        ),
                        style={
                            'flex': '1',
                            'padding': '10px',
                            'borderRadius': '5px'
                        }
                    )
                ]
            ),
            html.Div(  # Speed gauge and throttle bar section
                style={
                    'display': 'flex',
                    'flexDirection': 'row',  # Arrange horizontally
                    'gap': '100px',  # Add space between components
                    'justifyContent': 'left'
                },
                children=[
                    html.Div(  # Speed Gauge container
                        daq.Gauge(
                            showCurrentValue=True,
                            id="speed-display",
                            units="KMH",
                            value=0,
                            label='SPEED',
                            max=350,
                            min=0,
                            style={'width': '200px', 'height': '200px'}
                        ),
                        style={'textAlign': 'center'}
                    ),
                    html.Div(  # Speed Gauge container
                        daq.Gauge(
                            showCurrentValue=True,
                            id="rpm-display",
                            units="RPM",
                            value=0,
                            label='RPM',
                            max=15000,
                            min=0,
                            style={'width': '200px', 'height': '200px'}
                        ),
                        style={'textAlign': 'center'}
                    ),
                    html.Div(  # Throttle Bar container
                        daq.GraduatedBar(
                            showCurrentValue=True,
                            vertical=True,
                            id="throttle-display",
                            value=0,
                            label='THROTTLE',
                            max=100,
                            min=0,
                            color="blue"
                            # style={'width': '50px', 'height': '200px'}
                        ),
                        # style={'textAlign': 'center'}
                    )
                ]
            ),
            dcc.Store(id="selected-driver", data="Driver 55"),  # Default selected driver
            dcc.Interval(  # Interval component for updates
                id='interval-component',
                interval=500,  # Time interval in milliseconds
                n_intervals=0
            )
        ]
    )
