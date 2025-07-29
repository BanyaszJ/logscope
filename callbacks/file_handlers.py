"""
File handling callbacks for upload and browse functionality.
"""

import asammdf
import base64
import io
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
    def handle_file_upload(filenames, file_path):
        """Store the file path and metadata."""
        if not filenames or not file_path:
            return {}, ""

        files_data = {
            'filenames': filenames,
            'file_path': file_path,
            'upload_time': pd.Timestamp.now().isoformat()
        }

        return files_data, f"File path stored: {file_path}"

    @app.callback(
        Output('file-path-input', 'placeholder'),
        [Input('browse-button', 'n_clicks')]
    )
    def handle_browse_click(n_clicks):
        """Handle browse button click (placeholder functionality)."""
        if n_clicks:
            return "Browse functionality will be implemented..."
        return 'Enter file path or drag & drop files here...'

    # @app.callback(
    #     Output('placeholder', 'children'),  # Replace 'output-div' with your desired output component
    #     [Input('uploaded-files-store', 'data')]
    # )
    # def on_uploaded_files_store_change(data):
    #     """Execute logic when 'uploaded-files-store' changes."""
    #     if not data:
    #         return None
    #
    #     _mdf_object = asammdf.MDF(r'd:\_work\debug.mdf')  # Assuming first file is the MDF file
    #     _mdf_dataframe = _mdf_object.to_dataframe()
    #     _mdf_dataframe_idx = _mdf_dataframe.index
    #
    #     filenames = data.get('filenames', [])
    #     upload_time = data.get('upload_time', "Unknown")
    #     print(f"Signals in mdf: {_mdf_dataframe.columns.tolist()}", flush=True)
    #     return f"Files uploaded: {', '.join(filenames)} at {upload_time}"\
    #            f"mdf object: {_mdf_object}"\
    #            f"Signals in MDF: {', '.join(_mdf_dataframe.columns.tolist())}" \
    #            f"DataFrame index: {_mdf_dataframe_idx}"
