"""
Left panel layout containing file upload, data fields, and Python console.
"""

from dash import html
from styles.styles import LEFT_PANEL
from components.file_upload import create_file_upload_section
from components.data_fields import create_data_fields_section
from components.python_console import create_python_console_section


def create_left_panel():
    """Create the left panel with all its components."""
    return html.Div([
        create_file_upload_section(),
        create_data_fields_section(),
        create_python_console_section()
    ], style=LEFT_PANEL, id='left-panel')