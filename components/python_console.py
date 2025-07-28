"""
Python console component for executing Python commands.
"""

from dash import dcc, html
from styles.styles import (
    SECTION_CONTAINER, SECTION_HEADER,
    PYTHON_CONSOLE_INPUT, EXECUTE_BUTTON, PYTHON_OUTPUT
)


def create_python_console_section():
    """Create the Python console section with input, buttons, and output."""

    # Clear button style (similar to execute but different color)
    clear_button_style = EXECUTE_BUTTON.copy()
    clear_button_style.update({
        'backgroundColor': '#dc3545',  # Red color
        'marginLeft': '10px'
    })

    return html.Div([
        html.H4("Python Console", style=SECTION_HEADER),
        html.Div([
            dcc.Textarea(
                id='python-cmd-input',
                placeholder='>>> Enter Python commands here...\n# Examples:\n# !pip install numpy\n# import numpy as np\n# x = [1, 2, 3, 4, 5]\n# print(sum(x))\n# y = [i**2 for i in x]',
                style=PYTHON_CONSOLE_INPUT
            ),
            html.Div([
                html.Button(
                    'Execute',
                    id='execute-python-btn',
                    style=EXECUTE_BUTTON
                ),
                html.Button(
                    'Clear',
                    id='clear-python-btn',
                    style=clear_button_style
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ]),
        html.Div(
            id='python-output',
            style=PYTHON_OUTPUT
        ),
        html.Div(
            id='python-variables',
            style={
                'marginTop': '10px',
                'padding': '8px',
                'backgroundColor': '#e9ecef',
                'border': '1px solid #dee2e6',
                'borderRadius': '4px',
                'fontSize': '11px',
                'fontFamily': 'Consolas, Monaco, monospace',
                'maxHeight': '100px',
                'overflowY': 'auto'
            }
        )
    ], style=SECTION_CONTAINER)