"""
Data processing callbacks for handling string lists and data fields.
"""

from dash import Input, Output


def register_data_callbacks(app):
    """Register data processing callbacks."""

    @app.callback(
        [Output('string-list-store', 'data'),
         Output('string-list-output', 'children')],
        [Input('string-list-field', 'value')]
    )
    def process_string_list(text_input):
        """Process string list input and update store and display."""
        if not text_input:
            return [], "No items entered"

        # Split by lines and clean up
        string_list = [line.strip() for line in text_input.split('\n') if line.strip()]

        preview = ', '.join(string_list[:3])
        if len(string_list) > 3:
            preview += '...'

        return string_list, f"Items: {len(string_list)} | Preview: {preview}"