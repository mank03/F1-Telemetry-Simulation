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
            'padding': '10px',
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
                            'backgroundColor': '#black',
                            'padding': '0px',
                            'borderRadius': '5px',
                            'width': '250px',
                            'height': '600px',
                            'overflowY': 'auto'  # Allow scrolling for many drivers
                        },
                        children=[
                            html.H2("Drivers", style={'textAlign': 'center', "marginBottom" : "30px"}),
                            html.Div(id="leaderboard-content"),  # Populated by callback
                            dcc.Input(id="time-stamp-display", type="text", value="Time: ", disabled=True)
                        ]
                    ),
                    html.Div(  # Circuit map container
                        children=[
                            dcc.Graph(
                                id="circuit-map",
                                config={'displayModeBar': False, "scrollZoom": True},
                                style={'flex': '1', 'background-color': '#20242c'}
                            ),
                            dcc.Dropdown(
                                id="meeting-key-dropdown",
                                options=[
                                    {"label": "Singapore", "value": 1219},
                                ],
                                placeholder="Select a track",
                                value=1219,  # Default to Sinagpore
                                style={"marginBottom": "10px"}
                            ),
                            dcc.Dropdown(
                                id="session-key-dropdown",
                                options=[
                                    {"label": "Race", "value": 9165},
                                ],
                                placeholder="Select session type",
                                value=9165,  # Default to race
                                style={"marginBottom": "10px"}
                            ),
                            html.Button(
                                "GO",
                                id="apply-button",
                                style={"width": "100%", "marginTop": "10px"}
                            )
                        ],
                        style={
                            'flex': '1',
                            'padding': '0px',
                            'borderRadius': '0px',
                            'background-color': '#20242c'
                        }
                    )
                ]
            ),
            html.Div(  # Speed gauge, rpm gauge throttle bar, brake bar, Lap, and tyre display
                style={
                    'display': 'flex',
                    'flexDirection': 'row',  # Arrange horizontally
                    'gap': '75px',  # Add space between components
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
                    html.Div(  # RPM Gauge container
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
                            # style={'width': '50px', 'height': '200px'}
                        ),
                        # style={'textAlign': 'center'}
                    ),
                    html.Div(  # Brake Bar container
                        daq.GraduatedBar(
                            showCurrentValue=False,
                            vertical=True,
                            id="brake-display",
                            value=0,
                            step=100,
                            label='BRAKE',
                            max=100,
                            min=0,
                            color="red",
                            
                            # style={'width': '50px', 'height': '200px'}
                        )
                        # style={'textAlign': 'center'}
                    ),
                    html.Div(  # Lap display container
                        style={
                            'display': 'flex',
                            'flexDirection': 'row',
                            'gap': '20px',  # Custom gap for Lap and Tyre display
                            'justifyContent': 'left'
                        },
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        html.H3("Lap: 0", id="lap-number-display", style={"textAlign": "center", "color": "white"}),
                                    ),
                                    html.Div(  # Right section: Stint
                                        children=[
                                            html.H5("Stint: 1", id="stint-display", style={"textAlign": "center", "color": "white", "marginTop": "1px"})
                                        ],
                                        style={
                                            "display": "flex",
                                            "alignItems": "left",  # Center align the stint text vertically
                                            "justifyContent": "left",
                                            "marginRight": "20px"  # Add spacing to the right for the stint section
                                        }
                                    ),
                                    html.Div(
                                        html.H5("Lap Duration: 0:00.00", id="lap-duration-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                    ),
                                    html.Div(
                                        html.H5("Sector #1: 0:00.00", id="duration-sector-one-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                    ),
                                    html.Div(
                                        html.H5("Sector #2: 0:00.00", id="duration-sector-two-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                    ),
                                    html.Div(
                                        html.H5("Sector #3: 0:00.00", id="duration-sector-three-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                    )
                                ],
                                style=
                                {
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "alignItems": "left",
                                    "width": "225px",  # Updated width for the container
                                    "height": "310px",  # Updated width for the container
                                    "padding": "7px",  # Add padding for better spacing inside the container
                                    "backgroundColor": "#2c2f36",  # Background color for better contrast with shadow
                                    "borderRadius": "10px",  # Rounded corners
                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)"  # Shadow effect
                                }
                            ),
                            html.Div(  # tyre display container
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(  # Left section: Compound and image
                                                children=[
                                                    html.H5("Compound: ", id="compound-display", style={"textAlign": "center", "color": "white"}),
                                                    html.Img(id="compound-image", src="/assets/unknown.png", style={"height": "100px", "width": "100px"}),
                                                ],
                                                style={
                                                    "display": "flex",  # Align both sections (Compound/Image and Stint) side by side
                                                    "flexDirection": "column",  # Row layout
                                                    "alignItems": "center",  # Vertically center content
                                                    "justifyContent": "center",  # Center align items vertically
                                                    "padding": "0px",  # Add padding for better spacing inside the container
                                                    "backgroundColor": "#2c2f36",  # Background color for better contrast
                                                    "borderRadius": "10px",  # Rounded corners
                                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",  # Shadow effect
                                                    "width": "125px",  # Adjust width for your container
                                                    "height": "180px"
                                                }
                                            ),
                                            html.Div(  # Left section: Compound and image
                                                children=[
                                                    html.Div(
                                                        html.H5("Pits: 0", id="pit-number-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                                    ),
                                                    html.Div(
                                                        html.H5("Pit Lap: ", id="pit-lap-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                                    ),
                                                    html.Div(
                                                        html.H5("Pit Duration: ", id="pit-duration-display", style={"textAlign": "left", "color": "white", "marginTop": "1px"}),
                                                    ),
                                                ],
                                                 style={
                                                    "marginTop": "5px",
                                                    "display": "flex",  # Align both sections (Compound/Image and Stint) side by side
                                                    "flexDirection": "column",  # Row layout
                                                    "alignItems": "center",  # Vertically center content
                                                    "justifyContent": "center",  # Center align items vertically
                                                    "padding": "0px",  # Add padding for better spacing inside the container
                                                    "backgroundColor": "#2c2f36",  # Background color for better contrast
                                                    "borderRadius": "10px",  # Rounded corners
                                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",  # Shadow effect
                                                    "width": "125px",  # Adjust width for your container
                                                    "height": "140px"
                                                }
                                            )
                                        ],
                                    )
                                ],
                            ),
                            html.Div(  # race updates display container
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div(  # Left section: Compound and image
                                                children=[
                                                    html.Div(
                                                        html.H3("RACE UPDATES", style={"textAlign": "center", "color": "white"}),
                                                    ),
                                                    html.Div(
                                                        children=[
                                                            html.Div(
                                                                html.H5("Category: ", id = "category-display", style={"textAlign": "left", "color": "white", "marginTop": "1px", "marginRight": "60px"}),
                                                             ),
                                                            html.Div(
                                                                html.Img(id = "category-image", src="/assets/soft_compound.png", style={"alignItems": "right", "height": "65px", "width": "65px"}),
                                                            )
                                                        ],
                                                        style={
                                                        "display": "flex",  # Align both sections (Compound/Image and Stint) side by side
                                                        "flexDirection": "row",  # Row layout
                                                        "alignItems": "left",  # Vertically center content
                                                        "justifyContent": "left",  # Center align items vertically
                                                        "padding": "7px",  # Add padding for better spacing inside the container
                                                        }
                                                    ),
                                                    html.Div(
                                                        html.H5("Message: ", id = "race-message-display", style={"textAlign": "left", "color": "white", "marginTop": "20px", "marginLeft": "3px"}),
                                                    )
                                                ],
                                                 style={
                                                    "display": "flex",  # Align both sections (Compound/Image and Stint) side by side
                                                    "flexDirection": "column",  # Row layout
                                                    "alignItems": "left",  # Vertically center content
                                                    "justifyContent": "left",  # Center align items vertically
                                                    "padding": "7px",  # Add padding for better spacing inside the container
                                                    "backgroundColor": "#2c2f36",  # Background color for better contrast
                                                    "borderRadius": "10px",  # Rounded corners
                                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",  # Shadow effect
                                                    "width": "300px",  # Adjust width for your container
                                                    "height": "310px"
                                                }
                                            )
                                        ],
                                    )
                                ],
                            ),
                            html.Div(  # tyre display container
                                children=[
                                    html.Div(
                                        children=[
                                            html.Div( 
                                                children=[
                                                    html.H5("DRS: ", id = "drs-display", style={"textAlign": "center", "color": "white"}),
                                                ],
                                                style={
                                                    "display": "flex",  # Align both sections (Compound/Image and Stint) side by side
                                                    "flexDirection": "row",  # Row layout
                                                    "alignItems": "center",  # Vertically center content
                                                    "justifyContent": "center",  # Center align items vertically
                                                    "padding": "0px",  # Add padding for better spacing inside the container
                                                    "backgroundColor": "#2c2f36",  # Background color for better contrast
                                                    "borderRadius": "10px",  # Rounded corners
                                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",  # Shadow effect
                                                    "width": "175px",  # Adjust width for your container
                                                    "height": "50px"
                                                }
                                            ),
                                        ],
                                    )
                                ],
                            )
                        ]
                    )
                ]
            ),
            dcc.Store(id="selected-driver", data="Driver 55"),  # Default selected driver
            dcc.Store(id="saved-zoom", data={}),
            dcc.Store(id="telemetry-data", storage_type="memory"),
            dcc.Interval(  # Interval component for updates
                id='interval-component',
                interval=1000,  # Time interval in milliseconds
                n_intervals=0
            )
        ]
    )
