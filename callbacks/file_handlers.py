"""
File handling callbacks for upload and browse functionality.
"""

import asammdf
import base64
import os
import tempfile
import pandas as pd
from dash import Input, Output, State, callback_context, html
from dash.exceptions import PreventUpdate
import uuid


def register_file_callbacks(app):
    """Register file handling callbacks."""

    # Add clientside callback to prevent text input clicks from opening file dialog
    app.clientside_callback(
        """
        function(id) {
            setTimeout(() => {
                const upload = document.getElementById('file-upload-area');
                const input = document.getElementById('file-path-input');
                const button = document.getElementById('browse-button');
                
                if (upload && input) {
                    // Store the original onclick
                    const originalClick = upload.onclick;
                    
                    // Override the upload area's click handler
                    upload.onclick = function(e) {
                        // Only trigger file dialog if clicking the browse button
                        if (e.target === button || button.contains(e.target)) {
                            if (originalClick) originalClick.call(this, e);
                        }
                    };
                    
                    // Prevent input clicks from bubbling up
                    input.onclick = function(e) {
                        e.stopPropagation();
                    };
                }
            }, 100);
            return window.dash_clientside.no_update;
        }
        """,
        Output('file-path-input', 'style'),  # Dummy output
        Input('file-upload-area', 'id')
    )

    # Main file handling callback
    @app.callback(
        [Output('uploaded-files-store', 'data'),
         Output('file-path-input', 'value'),
         Output('string-list-field', 'value'),
         Output('file-upload-area', 'contents'),  # Clear contents to allow re-upload
         Output('file-upload-area', 'filename')],  # Clear filename too
        [Input('file-upload-area', 'contents'),
         Input('file-path-input', 'n_submit')],  # Manual path entry
        [State('file-upload-area', 'filename'),
         State('file-path-input', 'value'),
         State('uploaded-files-store', 'data')]
    )
    def handle_file_operations(contents, n_submit,
                              filename, manual_path, current_store):
        """Handle all file operations: browse, drag-drop, and manual entry."""

        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Initialize returns - always clear upload contents to allow re-upload
        files_data = current_store or {}
        path_display = manual_path or ""
        signals_text = ""

        # Handle manual path entry (on Enter key)
        if trigger_id == 'file-path-input' and n_submit:
            if manual_path and manual_path.strip():
                # Force processing even if it's the same file
                file_id = str(uuid.uuid4())
                result = process_mdf_file(manual_path.strip(), 'manual', file_id=file_id)
                if result['success']:
                    files_data = result['data']
                    path_display = manual_path.strip()
                    signals_text = result['signals_text']
                else:
                    signals_text = f"Error: {result['error']}"
            return files_data, path_display, signals_text, None, None

        # Handle file upload (browse or drag-and-drop)
        elif trigger_id == 'file-upload-area' and contents:
            # Generate unique ID for this upload
            file_id = str(uuid.uuid4())

            # Check file extension
            if not filename.lower().endswith(('.mdf', '.mf4', '.dat')):
                error_msg = f"Error: Only MDF files are supported (got {filename})"
                return files_data, path_display, error_msg, None, None

            # Save uploaded file to temp location
            temp_path = save_uploaded_file(contents, filename, file_id)
            if temp_path:
                result = process_mdf_file(temp_path, 'upload', original_filename=filename, file_id=file_id)
                if result['success']:
                    files_data = result['data']
                    path_display = temp_path
                    signals_text = result['signals_text']
                else:
                    signals_text = f"Error: {result['error']}"
                    # Clean up temp file on error
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except:
                            pass
            else:
                signals_text = "Error: Failed to save uploaded file"

        # Always clear contents to allow re-upload of same file
        return files_data, path_display, signals_text, None, None

    # Store MDF processing results in a separate store
    @app.callback(
        Output('uploaded-file-mdf-data', 'data'),
        [Input('uploaded-files-store', 'data')]
    )
    def update_mdf_data_store(files_data):
        """Update MDF data store when a new file is loaded."""
        if files_data and 'signal_names' in files_data:
            return {
                'file_path': files_data.get('file_path'),
                'signal_names': files_data.get('signal_names'),
                'signal_count': files_data.get('signal_count'),
                'groups_count': files_data.get('groups_count'),
                'mdf_version': files_data.get('mdf_version'),
                'processed_time': files_data.get('processed_time'),
                'file_id': files_data.get('file_id')
            }
        return {}

    # Update the file path input placeholder
    @app.callback(
        Output('file-path-input', 'placeholder'),
        [Input('uploaded-files-store', 'data')]
    )
    def update_placeholder(files_data):
        """Update placeholder based on current state."""
        if files_data and files_data.get('file_path'):
            basename = os.path.basename(files_data.get('file_path', ''))
            signal_count = files_data.get('signal_count', 0)
            return f'Current: {basename} ({signal_count} signals) | Enter new path...'
        return 'Enter MDF file path and press Enter...'

    # Visual feedback for drag and drop
    @app.callback(
        Output('file-upload-area', 'style'),
        [Input('file-upload-area', 'contents')],
        [State('file-upload-area', 'style')]
    )
    def update_upload_style(contents, current_style):
        """Update upload area style when file is dropped."""
        if contents:
            # Brief visual feedback
            return current_style
        return current_style


def save_uploaded_file(contents, filename, file_id):
    """Save uploaded file content to a temporary location."""
    try:
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(tempfile.gettempdir(), 'logscope_uploads')
        os.makedirs(temp_dir, exist_ok=True)

        # Clean up old files (older than 1 hour)
        cleanup_old_files(temp_dir, max_age_hours=1)

        # Generate unique filename using the file_id
        name_part, ext = os.path.splitext(filename)
        unique_filename = f"{name_part}_{file_id[:8]}{ext}"
        temp_path = os.path.join(temp_dir, unique_filename)

        # Decode and save file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        with open(temp_path, 'wb') as f:
            f.write(decoded)

        print(f"File saved to: {temp_path}", flush=True)
        return temp_path

    except Exception as e:
        print(f"Error saving file: {str(e)}", flush=True)
        return None


def cleanup_old_files(temp_dir, max_age_hours=1):
    """Clean up old temporary files."""
    try:
        current_time = pd.Timestamp.now()
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath):
                file_time = pd.Timestamp(os.path.getmtime(filepath), unit='s')
                if (current_time - file_time).total_seconds() > max_age_hours * 3600:
                    try:
                        os.remove(filepath)
                        print(f"Cleaned up old file: {filename}", flush=True)
                    except:
                        pass
    except Exception as e:
        print(f"Error during cleanup: {e}", flush=True)


def process_mdf_file(file_path, source, original_filename=None, file_id=None):
    """Process MDF file and extract signal names."""
    result = {
        'success': False,
        'data': {},
        'signals_text': '',
        'status': '',
        'error': None
    }

    try:
        # Verify file exists
        if not os.path.exists(file_path):
            result['error'] = f"File not found: {file_path}"
            return result

        # Verify it's an MDF file
        if not file_path.lower().endswith(('.mdf', '.mf4', '.dat')):
            result['error'] = f"Not an MDF file: {file_path}"
            return result

        print(f"Loading MDF file: {file_path}", flush=True)

        # Load MDF file
        mdf = asammdf.MDF(file_path)

        # Extract all signal names - improved method
        signal_names = []

        # Method 1: Use list_channels() if available
        try:
            channels_info = mdf.list_channels()
            if channels_info:
                signal_names = list(channels_info.keys())
        except AttributeError:
            pass

        # Method 2: Iterate through groups and channels
        if not signal_names:
            for group_idx, group in enumerate(mdf.groups):
                for channel in group.channels:
                    if hasattr(channel, 'name') and channel.name:
                        signal_names.append(channel.name)

        # Method 3: Try to_dataframe as last resort
        if not signal_names:
            try:
                df = mdf.to_dataframe(time_as_date=False)
                signal_names = [col for col in df.columns if col != 'timestamps']
            except Exception as e:
                print(f"Warning: Could not convert to dataframe: {e}", flush=True)

        # Remove duplicates while preserving order
        seen = set()
        unique_signals = []
        for signal in signal_names:
            if signal and signal not in seen:
                seen.add(signal)
                unique_signals.append(signal)

        signal_names = unique_signals

        # Format signals for display
        signals_text = '\n'.join(signal_names) if signal_names else 'No signals found'

        # Get file info
        file_stats = os.stat(file_path)

        # Prepare metadata
        file_info = {
            'file_path': file_path,
            'source': source,
            'original_filename': original_filename or os.path.basename(file_path),
            'signal_names': signal_names,
            'signal_count': len(signal_names),
            'groups_count': len(mdf.groups),
            'mdf_version': getattr(mdf, 'version', 'Unknown'),
            'processed_time': pd.Timestamp.now().isoformat(),
            'file_size': file_stats.st_size,
            'file_id': file_id or str(uuid.uuid4())
        }

        # Close the MDF file
        mdf.close()

        result['success'] = True
        result['data'] = file_info
        result['signals_text'] = signals_text
        result['status'] = f"Loaded: {len(signal_names)} signals from {os.path.basename(file_path)}"

        print(f"Successfully processed MDF: {len(signal_names)} signals found", flush=True)

    except Exception as e:
        result['error'] = str(e)
        result['status'] = f"Error: {str(e)}"
        print(f"Error processing MDF: {str(e)}", flush=True)

    return result