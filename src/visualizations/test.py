import json
import dash
from dash import dcc, html
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Mapbox configuration
MAPBOX_STYLE_URL = "mapbox://styles/mkonnur/cm4omuz6e008m01s8446k9r6n"
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoibWtvbm51ciIsImEiOiJjbTRvaWNmankwazByMm1xNG5teHF6dG54In0.jCPJgwqG3medIN6WRrY9XA"

# Load GeoJSON data from file
with open("singapore.geojson", "r") as file:
    geojson_data = json.load(file)

# Extract line coordinates from GeoJSON
line_coordinates = geojson_data["features"][0]["geometry"]["coordinates"]
line_lons, line_lats = zip(*line_coordinates)

# Extract line coordinates from GeoJSON
line_coordinates = geojson_data["features"][0]["geometry"]["coordinates"]
line_lons, line_lats = zip(*line_coordinates)

# Create map figure
map_figure = go.Figure()

# Add GeoJSON line as a scattermapbox trace
map_figure.add_trace(
    go.Scattermapbox(
        lon=line_lons,
        lat=line_lats,
        mode="lines",
        line=dict(width=4, color="blue"),
        name=geojson_data["features"][0]["properties"]["Name"],
    )
)

# Configure map layout
map_figure.update_layout(
    mapbox={
        "style": MAPBOX_STYLE_URL,
        "accesstoken": MAPBOX_ACCESS_TOKEN,
        "center": {"lat": 1.2914199488663753, "lon": 103.85980662254117},
        "zoom": 15,
    },
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

# Dash layout
app.layout = html.Div(
    children=[
        html.H1("Map with Inline GeoJSON", style={"textAlign": "center"}),
        dcc.Graph(id="map", figure=map_figure),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
