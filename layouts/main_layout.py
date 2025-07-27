"""
Main layout structure for the Dash application.
Combines left and right panels with the draggable divider.
"""

from dash import html, dcc
from styles.styles import MAIN_CONTAINER, APP_CONTAINER, DIVIDER
from layouts.left_panel import create_left_panel
from layouts.right_panel import create_right_panel


def create_main_layout():
    """Create the main application layout."""
    return html.Div([
        # Main container with left and right sections
        html.Div([
            create_left_panel(),

            # Draggable divider
            html.Div(
                id='divider',
                style=DIVIDER
            ),

            create_right_panel()

        ], style=MAIN_CONTAINER),

        # Hidden stores for data
        dcc.Store(id='uploaded-files-store'),
        dcc.Store(id='string-list-store'),
        dcc.Store(id='python-context-store')

    ], style=APP_CONTAINER)