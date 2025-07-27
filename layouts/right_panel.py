"""
Right panel layout containing the data visualization.
"""

from dash import html
from styles.styles import RIGHT_PANEL, SECTION_HEADER
from components.visualization import create_visualization_section


def create_right_panel():
    """Create the right panel with visualization."""
    return html.Div([
        html.H4("Data Visualization", style=SECTION_HEADER),
        create_visualization_section()
    ], style=RIGHT_PANEL, id='right-panel')