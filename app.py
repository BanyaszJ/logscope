"""
App factory and configuration.
Creates the Dash app instance and registers all components and callbacks.
"""

import dash
from layouts.main_layout import create_main_layout
from callbacks import register_all_callbacks


def create_app():
    """Create and configure the Dash application."""
    app = dash.Dash(__name__)

    app.layout = create_main_layout()
    register_all_callbacks(app)

    return app