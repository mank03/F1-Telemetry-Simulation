# This file defines and registers all callback function
from datetime import datetime
import json
from dash.dependencies import Input, Output, State, ALL
# from tkinter import ALL
from dash import dcc, html

import time
import vlc
import dash
from matplotlib import figure
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from telemetry import get_location_data, get_car_data, get_lap_data, get_stints_data, get_pit_data, get_race_control_data, get_radio_data, get_interval_data, get_position_data

# Mapbox access token (replace with your token)
MAPBOX_STYLE_URL = "mapbox://styles/mkonnur/cm4omuz6e008m01s8446k9r6n"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWtvbm51ciIsImEiOiJjbTRvaWNmankwazByMm1xNG5teHF6dG54In0.jCPJgwqG3medIN6WRrY9XA"

LAT_REF = 1.29148788242174
LON_REF = 103.85494601254759
X_REF = -9465
Y_REF = 540
LAT_SCALE = 2.933e-6  # Calculated earlier
LON_SCALE = 8.835e-7  # Calculated earlier

# Play audio using VLC
def play_audio(url):
    player = vlc.MediaPlayer(url)
    player.play()
    while True:
        state = player.get_state()
        if state in (vlc.State.Ended, vlc.State.Error):
            break
        time.sleep(0.1)  # Avoid busy-waiting

# Load GeoJSON data from file
with open("singapore.geojson", "r") as file:
    geojson_data = json.load(file)

# Extract line coordinates from GeoJSON
line_coordinates = geojson_data["features"][0]["geometry"]["coordinates"]
line_lons, line_lats = zip(*line_coordinates)

# Fetch telemetry data
telemetry_data = {
    "Driver 55": {
        "location": get_location_data(9165, 1219, 55),
        "car": get_car_data(9165, 1219, 55),
        "lap": get_lap_data(9165, 1219, 55),
        "stint": get_stints_data(9165, 1219, 55),
        "pit": get_pit_data(9165, 1219, 55),
        "radio": get_radio_data(9165, 1219, 55),
        "interval": get_interval_data(9165, 1219, 55),
        "position": get_position_data(9165, 1219, 55)
    },
    "Driver 4": {
        "location": get_location_data(9165, 1219, 4),
        "car": get_car_data(9165, 1219, 4),
        "lap": get_lap_data(9165, 1219, 4),
        "stint": get_stints_data(9165, 1219, 4),
        "pit": get_pit_data(9165, 1219, 4),
        "radio": get_radio_data(9165, 1219, 4),
        "interval": get_interval_data(9165, 1219, 4),
        "position": get_position_data(9165, 1219, 4)
    },
        "Driver 44": {
        "location": get_location_data(9165, 1219, 44),
        "car": get_car_data(9165, 1219, 44),
        "lap": get_lap_data(9165, 1219, 44),
        "stint": get_stints_data(9165, 1219, 44),
        "pit": get_pit_data(9165, 1219, 44),
        "radio": get_radio_data(9165, 1219, 44),
        "interval": get_interval_data(9165, 1219, 44),
        "position": get_position_data(9165, 1219, 44)
    },
    "Race Updates": {
        "race_control": get_race_control_data(9165, 1219)
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
x_coords_44, y_coords_44   = get_driver_coordinates("Driver 44", telemetry_data)
x_coords_55, y_coords_55   = get_driver_coordinates("Driver 55", telemetry_data)

# # Extract data for visualization
# x_coords_55 = [point["x"] for point in telemetry_driver_55]
# y_coords_55 = [point["y"] for point in telemetry_driver_55]

compound_images = {
    "MEDIUM": "/assets/medium_compound.png",
    "HARD": "/assets/hard_compound.png",
    "SOFT": "/assets/soft_compound.png",
    "UNKNOWN": "/assets/unknown_compound.png"
}

category_images = {
    "SafetyCar": "/assets/SafetyCar.gif",
    "Other": "/assets/other.png",
    "Flag": "/assets/yellow.png",
    "UNKNOWN": "/assets/other.png"
}

flag_images = {
    "GREEN": "/assets/green.png",
    "YELLOW": "/assets/yellow.png",
    "CHEQUERED": "/assets/chequered.svg",
    "BLACK AND WHITE": "/assets/black_white.avif",
    "RED": "/assets/red.png",
    "CLEAR": "/assets/green.png",
    "BLUE": "/assets/blue.webp",
    'BLACK': "/assets/black.png",
    'WHITE': "/assets/white/png",
    "UNKNOWN": "/assets/other.png"
}

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
        leaderboard_data = ["Driver 55", "Driver 4", "Driver 44"]  # Ordered list of drivers
        return leaderboard_data[index] if index is not None else current_selection
        
    @app.callback(
        [
            Output("circuit-map", "figure"),
            Output("speed-display", "value"),
            Output("throttle-display", "value"),
            Output("brake-display", "value"),
            Output("rpm-display", "value"),
            Output("lap-number-display", "children"),
            Output("lap-duration-display", "children"),
            Output("duration-sector-one-display", "children"),
            Output("duration-sector-two-display", "children"),
            Output("duration-sector-three-display", "children"),
            Output("time-stamp-display", "value"),
            Output("leaderboard-content", "children"),
            Output("saved-zoom", "data"),  # Store zoom state in a dcc.Store
            Output("stint-display", "children"),
            Output("compound-display", "children"),
            Output("compound-image", "src"),
            Output("pit-number-display", "children"),
            Output("pit-lap-display", "children"),
            Output("pit-duration-display", "children"),
            Output("race-message-display", "children"),
            Output("category-display", "children"),
            Output("category-image", "src"),
            Output("drs-display", "children")
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
        stint_data = telemetry_data[selected_driver]["stint"]
        pit_data = telemetry_data[selected_driver]["pit"]
        race_control_data = telemetry_data["Race Updates"]["race_control"]
        radio_data = telemetry_data[selected_driver]["radio"]
        interval_data_55 = telemetry_data["Driver 55"]["interval"]
        interval_data_4 = telemetry_data["Driver 4"]["interval"]
        interval_data_44 = telemetry_data["Driver 44"]["interval"]
        position_data_55 = telemetry_data["Driver 55"]["position"]
        position_data_4 = telemetry_data["Driver 4"]["position"]
        position_data_44 = telemetry_data["Driver 44"]["position"]

        # Extract data for visualization
        x_coords = [point["x"] for point in location_data]
        y_coords = [point["y"] for point in location_data]
        time_stamps = [point["date"] for point in location_data]
        lap_time_stamps = [point["date_start"] for point in lap_data]
        lap_duration = [point["lap_duration"] for point in lap_data]
        duration_sector_one = [point["duration_sector_1"] for point in lap_data]
        duration_sector_two = [point["duration_sector_2"] for point in lap_data]
        duration_sector_three = [point["duration_sector_3"] for point in lap_data]

        tyre_compound = [point["compound"] for point in stint_data]
        stint_lap_start = [point["lap_start"] for point in stint_data]
        stint_lap_end = [point["lap_end"] for point in stint_data]
        stints = [point["stint_number"] for point in stint_data]    
        # time_stamps = lap_time_stamps

        
       # Get the current timestamp
        time_index = 15000 + n_intervals % len(time_stamps)
        lap_time_index = n_intervals % len(time_stamps)

        time_index_55 = 15000 + n_intervals % len(x_coords_55)
        time_index_4 = 15000 + n_intervals % len(x_coords_4)
        current_timestamp = time_stamps[time_index]

        print("time_index = ", time_index)
        print("time_index_55 = ", time_index_55)
        print("time_index_4 = ", time_index_4)
        print("current_timestamp = ", time_stamps[time_index])
        
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

        if lap_duration[current_lap] == None:
            lap_duration[current_lap] = "00:00.00"

        if duration_sector_one[current_lap]  == None:
            duration_sector_one[current_lap] = "00:00.00"

        if duration_sector_two[current_lap]  == None:
            duration_sector_two[current_lap] = "00:00.00"

        if duration_sector_three[current_lap]  == None:
            duration_sector_three[current_lap] = "00:00.00"

        current_compound = tyre_compound[0]
        current_stint = 0
        pit_number = 0
        lap_of_pit = 0
        pit_duration = 0


        print("The # of pit stops are: ", len(pit_data))
        for idx, entry in enumerate(pit_data):  # Iterate through pit data
            print("pit - index: ", idx)
            print("pit - entry: ", entry)
            print("pit - entry[date]: ", entry["date"])

            # Check if the current timestamp is greater than or equal to the entry date
            if current_timestamp >= entry["date"]:
                lap_of_pit = entry["lap_number"]
                pit_duration = entry["pit_duration"]
                pit_number += 1
                # Update the current compound and stint number
                for stint in stints:
                    print("stint: ", stint)
                    print(f"stint_lap_start[{stint}] = {stint_lap_start[stint-1]}")
                    print(f"stint_lap_end[{stint}] = {stint_lap_end[stint-1]}")
                    if stint_lap_start[stint-1] <= (lap_of_pit + 1) <= stint_lap_end[stint-1]:
                        current_compound = tyre_compound[stint-1]
                        print("current_compound: ", current_compound)
                        current_stint = stint
                        break
                    else:
                        current_compound = "None"

                break  # Exit the loop once the condition is satisfied

        message = "None"
        for idx, entry in enumerate(race_control_data):  # Iterate through pit data
            if entry["date"] <= current_timestamp:
                message = entry["message"]
                category = entry["category"]
                flag = entry["flag"]

        if category in category_images:
            category_images_src = category_images[category]
        else:
            category_images_src = category_images["UNKNOWN"]

        if flag in flag_images:
            category_images_src = flag_images[flag]
        else:
            category_images_src = category_images["UNKNOWN"]

        # Output the result
        print(f"The driver is currently on lap {current_lap+1} and lap duration is {lap_duration[current_lap]}.")
        
        print(f"Sector #1: {duration_sector_one[current_lap]}, Sector #2: {duration_sector_two[current_lap]}, Sector #3: {duration_sector_three[current_lap]}.")

        print(f"Stint #: {current_stint}, Compound:  {current_compound}")

        # Get the compound image source
        if current_compound in compound_images:
            compound_image_src = compound_images[current_compound]
        else:
            compound_image_src = compound_images["UNKNOWN"]  # Default to "UNKNOWN"

        print("compound_image_src = ", compound_image_src)
        

        closest_data = min(
            car_data,
            key=lambda point: abs((datetime.fromisoformat(point["date"]).timestamp() - datetime.fromisoformat(current_timestamp).timestamp()))
        )
        speed = closest_data["speed"]  # Safely extract speed
        throttle = closest_data["throttle"]
        brake = closest_data["brake"]
        rpm = closest_data["rpm"]
        driver_number = closest_data["driver_number"]
        drs = closest_data["drs"]

        next_time_index = (time_index + 1) % len(x_coords)

        # Compute a fraction of the way between the current position and the next
        fraction = (n_intervals % 10) / 10  # Smooth transition over 10 intervals (100 ms each)

        x_position = x_coords[time_index] + fraction * (x_coords[next_time_index] - x_coords[time_index])
        y_position = y_coords[time_index] + fraction * (y_coords[next_time_index] - y_coords[time_index])

        # Print current positions for debugging
        print(f"Selected driver - #: {driver_number}, lat: {x_coords_55[time_index]}, lon: {y_coords_55[time_index]}, speed_55: {speed}, throttle_55: {throttle}, brake_55: {brake}, rpm_55: {rpm}, lap #: {current_lap+1}")
        
        if drs in {0, 1}:
            drs_message = "DISABLED"
        elif drs in {10, 12, 14}:
            drs_message = "ENABLED"
        else:
            drs_message = "Detected, not eligible"

        
        print("DRS: ", drs)

        
        recording = "None"

        for idx, entry in enumerate(radio_data):  # Iterate through pit data
            entry_datetime = datetime.fromisoformat(entry["date"])
            current_timestamp_new = datetime.fromisoformat(current_timestamp)
            if abs((current_timestamp_new - entry_datetime).total_seconds()) <= 0.5:
                recording = entry["recording_url"]
                print(f"Playing recording for driver {driver_number} at {entry["date"]}")
                play_audio(entry["recording_url"])
                break
        
        driver_interval_55 = "None"
        

        for idx, entry in enumerate(interval_data_55):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_interval_55 = entry["interval"]
        
        driver_position_55 = "None"

        for idx, entry in enumerate(position_data_55):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_position_55 = entry["position"]

        driver_interval_4 = "None"
        
        for idx, entry in enumerate(interval_data_4):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_interval_4 = entry["interval"]

        driver_position_4 = "None"
        
        for idx, entry in enumerate(position_data_4):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_position_4 = entry["position"]

        driver_interval_44 = "None"
        
        for idx, entry in enumerate(interval_data_44):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_interval_44 = entry["interval"]

        driver_position_44 = "None"
        
        for idx, entry in enumerate(position_data_44):  # Iterate through pit data
            entry_date = datetime.fromisoformat(entry["date"])
            current_timestamp_intervals = datetime.fromisoformat(current_timestamp)
            if current_timestamp_intervals >= entry_date:
                    driver_position_44 = entry["position"]
        # Leaderboard content
        leaderboard_data = [
            {
                "image": "/assets/sainz.avif",
                "name": "Carlos Sainz",
                "time": str(driver_interval_55) if driver_interval_55 is not None else "N/A",  # Use fallback if None
                "position": str(driver_position_55) if driver_position_55 is not None else "N/A",
                "id": "Driver 55",
            },
            {
                "image": "/assets/norris.avif",
                "name": "Lando Norris",
                "time": str(driver_interval_4) if driver_interval_4 is not None else "N/A",
                "position": str(driver_position_4) if driver_position_4 is not None else "N/A",
                "id": "Driver 4",
            },
            {
                "image": "/assets/hamilton.avif",
                "name": "Lewis Hamilton",
                "time": str(driver_interval_44) if driver_interval_44 is not None else "N/A",
                "position": str(driver_position_44) if driver_position_44 is not None else "N/A",
                "id": "Driver 44",
            },
        ]

        leaderboard_content = [
            html.Div(
                children=[
                    html.Img(
                        src=entry['image'],  # The image source from the data
                        alt=f"Image of {entry['name']}",
                        style={'width': '100px', 'height': '100px'}  # Adjust size and margin as needed
                    ),
                    html.Div(  # Wrap name and time in a div to stack them vertically
                        children=[
                            html.Span(f"{entry['name']}", style={'fontWeight': 'bold'}),
                            html.Span(f"{entry['time']}", style={'marginTop': '5px'}),  # Add margin-top to space out time from name
                            html.Span(f"{entry['position']}", style={'marginTop': '5px', 'fontSize': '20px'})  # Add margin-top to space out time from name
                        ],
                        style={'display': 'flex', 'flexDirection': 'column', 'marginLeft': '8px'}  # Stack name and time vertically
                    ),
                ],
                style={
                    'cursor': 'pointer',
                    'display': 'flex',
                    'alignItems': 'center',
                    "justifyContent": "left",
                    'padding': '2px',
                    'border': '1px solid white' if entry['id'] == selected_driver else 'transparent',
                    'backgroundColor': "#2c2f36" if entry['id'] == selected_driver else 'transparent',
                    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.5)' if entry['id'] == selected_driver else 'none',
                },
                id={"type": "leaderboard-item", "index": i},  # Use dictionary format for the id
                n_clicks=0
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
                ),
                go.Scattergl(  # Use scattergl for the other driver
                x=[x_coords_44[time_index]], 
                y=[y_coords_44[time_index]], 
                mode="markers", 
                name="Lewis Hamilton",
                marker=dict(size=10, color="#00A19C")
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

        return updated_map, speed, throttle, brake, rpm, f"Lap:\t{current_lap+1}", f"Lap Duration:\t{lap_duration[current_lap]}", f"Sector #1:    {duration_sector_one[current_lap]}", f"Sector #2:    {duration_sector_two[current_lap]}", f"Sector #3:   {duration_sector_three[current_lap]}", current_timestamp, leaderboard_content, saved_zoom, f"Stint: {current_stint}", current_compound, compound_image_src, f"Pits: {pit_number}", f"Pit Lap: {lap_of_pit}", f"Duration: {pit_duration}", f"Info: {message}", f"Category: {category}", category_images_src, f"DRS: {drs_message}"
