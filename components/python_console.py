"""
Python console component for executing Python commands.
"""

from dash import dcc, html
from styles.styles import (
    SECTION_CONTAINER, SECTION_HEADER,
    PYTHON_CONSOLE_INPUT, EXECUTE_BUTTON, PYTHON_OUTPUT
)


def create_python_console_section():
    """Create the Python console section with input, button, and output."""
    return html.Div([
        html.H4("Python Console", style=SECTION_HEADER),
        html.Div([
            dcc.Textarea(
                id='python-cmd-input',
                placeholder='>>> Enter Python commands here...\n# Example:\n# print("Hello World")\n# x = [1, 2, 3, 4]\n# sum(x)',
                style=PYTHON_CONSOLE_INPUT
            ),
            html.Button(
                'Execute',
                id='execute-python-btn',
                style=EXECUTE_BUTTON
            )
        ]),
        html.Div(
            id='python-output',
            style=PYTHON_OUTPUT
        )
    ], style=SECTION_CONTAINER)