"""
File handling callbacks for upload and browse functionality.
"""

import pandas as pd
from dash import Input, Output, State


def register_file_callbacks(app):
    """Register file handling callbacks."""

    @app.callback(
        [Output('uploaded-files-store', 'data'),
         Output('file-path-input', 'value')],
        [Input('file-upload-area', 'contents')],
        [State('file-upload-area', 'filename')]
    )
    def handle_file_upload(contents, filenames):
        """Handle file upload and update store and display."""
        if contents is None:
            return {}, ""

        # For now, just store the filename info
        files_data = {}
        if filenames:
            files_data = {
                'filenames': filenames,
                'upload_time': pd.Timestamp.now().isoformat()
            }
            return files_data, f"Uploaded: {', '.join(filenames)}"

        return {}, ""

    @app.callback(
        Output('file-path-input', 'placeholder'),
        [Input('browse-button', 'n_clicks')]
    )
    def handle_browse_click(n_clicks):
        """Handle browse button click (placeholder functionality)."""
        if n_clicks:
            return "Browse functionality will be implemented..."
        return 'Enter file path or drag & drop files here...'