# This file initializes the Dash app, imports the layout, and registers the callbacks

from dash import Dash
from layout import create_layout
from callbacks import register_callbacks

# Initialize the Dash application
app = Dash(__name__)

# Set the layout
app.layout = create_layout()

# Register the callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)