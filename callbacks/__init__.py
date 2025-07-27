"""
Callback registration module.
Imports and registers all callback modules.
"""

from .ui_interactions import register_ui_callbacks
from .file_handlers import register_file_callbacks
from .data_processing import register_data_callbacks
from .python_console import register_console_callbacks


def register_all_callbacks(app):
    """Register all application callbacks."""
    register_ui_callbacks(app)
    register_file_callbacks(app)
    register_data_callbacks(app)
    register_console_callbacks(app)