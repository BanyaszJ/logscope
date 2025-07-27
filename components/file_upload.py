"""
File upload component with drag-and-drop and browse functionality.
"""

from dash import dcc, html
from styles.styles import (
    SECTION_CONTAINER, FILE_UPLOAD_CONTAINER,
    FILE_PATH_INPUT, BROWSE_BUTTON
)


def create_file_upload_section():
    """Create the file upload section with drag-drop and browse."""
    return html.Div([
        # Combined file path input and drag-drop area
        dcc.Upload(
            id='file-upload-area',
            children=[
                dcc.Input(
                    id='file-path-input',
                    type='text',
                    placeholder='Enter file path or drag & drop files here...',
                    disabled=True,
                    style=FILE_PATH_INPUT
                ),
                # Browse button
                html.Button(
                    'Browse',
                    id='browse-button',
                    style=BROWSE_BUTTON
                )
            ],
            style=FILE_UPLOAD_CONTAINER,
            multiple=True
        )
    ], style=SECTION_CONTAINER)