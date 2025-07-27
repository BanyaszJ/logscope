"""
Data visualization component with plotly graph.
"""

from dash import dcc
import plotly.graph_objects as go
from styles.styles import PLOT_STYLE


def create_visualization_section():
    """Create the main plot visualization."""
    return dcc.Graph(
        id='main-plot',
        style=PLOT_STYLE,
        figure=create_default_figure()
    )


def create_default_figure():
    """Create the default empty figure with placeholder text."""
    return go.Figure().update_layout(
        title="Ready for Data",
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        template="plotly_white",
        annotations=[
            dict(
                text="Load data to display plots here",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=20, color="gray")
            )
        ]
    )