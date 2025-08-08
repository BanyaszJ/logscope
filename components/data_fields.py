"""
Enhanced signal list component with clickable and draggable signals.
"""

from dash import html, dcc
from styles.styles import (
    DATA_FIELDS_CONTAINER, SECTION_HEADER,
    DATA_OUTPUT
)


def create_data_fields_section():
    """Create the data fields section with interactive signal list."""
    return html.Div([
        html.H4("Signal List", style=SECTION_HEADER),
        html.Div(
            id='signal-list-container',
            children=[
                html.Div(
                    "Load an MDF file to see signals here",
                    style={
                        'padding': '20px',
                        'textAlign': 'center',
                        'color': '#666',
                        'fontStyle': 'italic'
                    }
                )
            ],
            style={
                'height': '300px',
                'overflowY': 'auto',
                'border': '1px solid #ddd',
                'borderRadius': '4px',
                'backgroundColor': 'white',
                'padding': '5px'
            }
        ),
        html.Div(
            id='string-list-output',
            style=DATA_OUTPUT
        ),
        html.Div([
            html.Small(
                "💡 Double-click signals to plot them",
                style={
                    'color': '#666',
                    'fontStyle': 'italic',
                    'fontSize': '11px'
                }
            )
        ], style={'marginTop': '5px'}),
        # Hidden textarea for backward compatibility
        dcc.Textarea(
            id='string-list-field',
            style={'display': 'none'}
        )
    ], style=DATA_FIELDS_CONTAINER)


def create_signal_item(signal_name, index):
    """Create an individual clickable signal item."""
    return html.Div(
        signal_name,
        id={'type': 'signal-item', 'index': index},
        className='signal-item',
        **{'data-signal-name': signal_name},
        style={
            'padding': '8px 12px',
            'margin': '2px 0',
            'backgroundColor': '#f8f9fa',
            'border': '1px solid #dee2e6',
            'borderRadius': '4px',
            'cursor': 'pointer',
            'userSelect': 'none',
            'fontSize': '13px',
            'fontFamily': 'monospace',
            'transition': 'all 0.2s ease'
        }
    )