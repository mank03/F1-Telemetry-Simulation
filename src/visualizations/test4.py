import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Sample telemetry data (replace this with actual data if available)
df = pd.DataFrame({
    'time': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'x': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],  # X coordinates of car
    'y': [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],    # Y coordinates of car
})

# Initialize Dash app
app = dash.Dash(__name__)

# Create the layout of the app with a graph component and an interval component
app.layout = html.Div([
    dcc.Graph(id='track-graph'),
    dcc.Interval(
        id='interval-update',
        interval=1000,  # Update every 1 second (1000 ms)
        n_intervals=0
    )
])

# Define the callback to update the car position on the graph
@app.callback(
    Output('track-graph', 'figure'),
    [Input('interval-update', 'n_intervals')]
)
def update_car_position(n):
    # Get current car position based on time
    current_data = df.iloc[n % len(df)]  # Loop over data if necessary
    
    # Create a scatter plot for the car's position
    car_trace = go.Scatter(
        x=df['x'][:n+1],  # Plot up to the current point
        y=df['y'][:n+1],  # Plot up to the current point
        mode='markers+lines',  # 'lines' shows movement, 'markers' shows the points
        name="F1 Car",
        marker=dict(color='red', size=10),
    )

    # Layout for the plot
    layout = go.Layout(
        title="F1 Driver's Car Position on Race Track",
        xaxis=dict(title='Track X', range=[0, 110]),  # Adjust range as needed
        yaxis=dict(title='Track Y', range=[0, 110]),  # Adjust range as needed
    )
    
    # Return the updated figure
    return {'data': [car_trace], 'layout': layout}

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
