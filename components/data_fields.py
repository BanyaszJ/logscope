"""
Data fields component for entering and managing field names.
"""

from dash import dcc, html
from styles.styles import (
    DATA_FIELDS_CONTAINER, SECTION_HEADER,
    DATA_TEXTAREA, DATA_OUTPUT
)


def create_data_fields_section():
    """Create the data fields section with textarea and output."""
    return html.Div([
        html.H4("Data Fields", style=SECTION_HEADER),
        dcc.Textarea(
            id='string-list-field',
            placeholder='Field 1\nField 2\nField 3',
            style=DATA_TEXTAREA
        ),
        html.Div(
            id='string-list-output',
            style=DATA_OUTPUT
        )
    ], style=DATA_FIELDS_CONTAINER)