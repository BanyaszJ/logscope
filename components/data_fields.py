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
        # Header with title and clear button
        html.Div([
            html.H4("Signal List", style={
                **SECTION_HEADER,
                'margin': '0',
                'flex': '1'
            }),
            html.Button(
                'Clear Plot',
                id='clear-plot-btn',
                style={
                    'padding': '8px 16px',
                    'backgroundColor': '#dc3545',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'fontSize': '13px',
                    'fontWeight': 'bold',
                    'minWidth': '90px',
                    'height': '36px'
                }
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'marginBottom': '10px'
        }),

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
                "💡 Click signals to plot them | Clear button removes all plots",
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
            'padding': '4px 8px',
            'margin': '1px 0',
            'cursor': 'pointer',
            'userSelect': 'none',
            'fontSize': '13px',
            'fontFamily': 'monospace',
            'color': '#333',
            'borderRadius': '3px'
        }
    )


def create_signal_item_with_state(signal_name, index, is_plotted=False):
    """Create an individual clickable signal item with plotted state styling."""
    base_style = {
        'padding': '4px 8px',
        'margin': '1px 0',
        'cursor': 'pointer',
        'userSelect': 'none',
        'fontSize': '13px',
        'fontFamily': 'monospace',
        'borderRadius': '3px'
    }

    # Apply different styles based on plotted state
    if is_plotted:
        base_style.update({
            'backgroundColor': '#007bff',
            'color': 'white'
        })
    else:
        base_style.update({
            'backgroundColor': 'transparent',
            'color': '#333'
        })

    return html.Div(
        signal_name,
        id={'type': 'signal-item', 'index': index},
        className='signal-item',
        **{'data-signal-name': signal_name},
        style=base_style
    )