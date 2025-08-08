"""
Enhanced data processing callbacks for handling signal interactions and plotting.
"""

import asammdf
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from components.data_fields import create_signal_item


def register_data_callbacks(app):
    """Register enhanced data processing callbacks."""

    # Update signal list when MDF file is loaded
    @app.callback(
        [Output('signal-list-container', 'children'),
         Output('string-list-store', 'data'),
         Output('string-list-output', 'children')],
        [Input('uploaded-files-store', 'data')]
    )
    def update_signal_list(files_data):
        """Update the signal list display when MDF file is loaded."""
        if not files_data or 'signal_names' not in files_data:
            empty_message = html.Div(
                "Load an MDF file to see signals here",
                style={
                    'padding': '20px',
                    'textAlign': 'center',
                    'color': '#666',
                    'fontStyle': 'italic'
                }
            )
            return [empty_message], [], "No signals loaded"

        signal_names = files_data['signal_names']
        
        # Create interactive signal items
        signal_items = []
        for i, signal_name in enumerate(signal_names):
            signal_items.append(create_signal_item(signal_name, i))

        # Update summary
        summary = f"Signals: {len(signal_names)} loaded from {files_data.get('original_filename', 'MDF file')}"
        
        return signal_items, signal_names, summary

    # Handle signal item clicks (double-click to plot)
    @app.callback(
        Output('main-plot', 'figure'),
        [Input({'type': 'signal-item', 'index': ALL}, 'n_clicks')],
        [State('uploaded-files-store', 'data'),
         State('main-plot', 'figure')]
    )
    def handle_signal_click(n_clicks_list, files_data, current_figure):
        """Handle signal item clicks to plot data."""
        if not callback_context.triggered or not files_data:
            raise PreventUpdate
            
        # Find which signal was clicked
        triggered_id = callback_context.triggered[0]['prop_id']
        if 'n_clicks' not in triggered_id:
            raise PreventUpdate
            
        # Extract the index from the triggered component
        import json
        component_id = json.loads(triggered_id.split('.')[0])
        signal_index = component_id['index']
        
        signal_names = files_data.get('signal_names', [])
        if signal_index >= len(signal_names):
            raise PreventUpdate
            
        signal_name = signal_names[signal_index]
        file_path = files_data.get('file_path')
        
        if not file_path:
            raise PreventUpdate
            
        # Load and plot the signal
        try:
            # Get file_id for caching
            file_id = files_data.get('file_id', 'default')
            figure = plot_signal(file_path, signal_name, current_figure, file_id)
            return figure
        except Exception as e:
            print(f"Error plotting signal {signal_name}: {e}")
            raise PreventUpdate

"""
Enhanced data processing callbacks for handling signal interactions and plotting.
"""

import asammdf
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from components.data_fields import create_signal_item


def register_data_callbacks(app):
    """Register enhanced data processing callbacks."""

    # Update signal list when MDF file is loaded
    @app.callback(
        [Output('signal-list-container', 'children'),
         Output('string-list-store', 'data'),
         Output('string-list-output', 'children')],
        [Input('uploaded-files-store', 'data')]
    )
    def update_signal_list(files_data):
        """Update the signal list display when MDF file is loaded."""
        if not files_data or 'signal_names' not in files_data:
            empty_message = html.Div(
                "Load an MDF file to see signals here",
                style={
                    'padding': '20px',
                    'textAlign': 'center',
                    'color': '#666',
                    'fontStyle': 'italic'
                }
            )
            return [empty_message], [], "No signals loaded"

        signal_names = files_data['signal_names']

        # Create interactive signal items
        signal_items = []
        for i, signal_name in enumerate(signal_names):
            signal_items.append(create_signal_item(signal_name, i))

        # Update summary
        summary = f"Signals: {len(signal_names)} loaded from {files_data.get('original_filename', 'MDF file')}"

        return signal_items, signal_names, summary

    # Handle signal item clicks (double-click to plot)
    @app.callback(
        Output('main-plot', 'figure'),
        [Input({'type': 'signal-item', 'index': ALL}, 'n_clicks')],
        [State('uploaded-files-store', 'data'),
         State('main-plot', 'figure')]
    )
    def handle_signal_click(n_clicks_list, files_data, current_figure):
        """Handle signal item clicks to plot data."""
        if not callback_context.triggered or not files_data:
            raise PreventUpdate

        # Find which signal was clicked
        triggered_id = callback_context.triggered[0]['prop_id']
        if 'n_clicks' not in triggered_id:
            raise PreventUpdate

        # Extract the index from the triggered component
        import json
        component_id = json.loads(triggered_id.split('.')[0])
        signal_index = component_id['index']

        signal_names = files_data.get('signal_names', [])
        if signal_index >= len(signal_names):
            raise PreventUpdate

        signal_name = signal_names[signal_index]
        file_path = files_data.get('file_path')

        if not file_path:
            raise PreventUpdate

        # Load and plot the signal
        try:
            figure = plot_signal(file_path, signal_name, current_figure)
            return figure
        except Exception as e:
            print(f"Error plotting signal {signal_name}: {e}")
            raise PreventUpdate

    # Clear cache when new file is loaded
    @app.callback(
        Output('placeholder', 'children'),  # Dummy output
        [Input('uploaded-files-store', 'data')]
    )
    def clear_cache_on_new_file(files_data):
        """Clear MDF cache when a new file is loaded."""
        # Only clear cache if this is actually a new file
        if files_data and 'file_id' in files_data:
            # Keep only the current file in cache, clear others
            current_file_id = files_data['file_id']
            current_path = files_data['file_path']
            current_key = f"{current_path}_{current_file_id}"

            keys_to_remove = [k for k in _mdf_cache.keys() if k != current_key]
            for key in keys_to_remove:
                try:
                    _mdf_cache[key].close()
                    del _mdf_cache[key]
                except:
                    pass

        return ""
    app.clientside_callback(
        """
        function(trigger) {
            // Set up interactions for signal items
            setTimeout(function() {
                const signalItems = document.querySelectorAll('.signal-item');
                
                signalItems.forEach(function(item) {
                    // Hover effects
                    item.addEventListener('mouseenter', function() {
                        this.style.backgroundColor = '#e3f2fd';
                        this.style.borderColor = '#1976d2';
                    });
                    
                    item.addEventListener('mouseleave', function() {
                        this.style.backgroundColor = '#f8f9fa';
                        this.style.borderColor = '#dee2e6';
                    });
                    
                    // Double-click handler
                    item.addEventListener('dblclick', function() {
                        // Trigger the click callback
                        item.click();
                    });
                });
            }, 100);
            
            return window.dash_clientside.no_update;
        }
        """,
        Output('signal-list-container', 'style'),
        Input('signal-list-container', 'children')
    )


# Global cache for MDF files to avoid re-opening
_mdf_cache = {}

def get_cached_mdf(file_path, file_id):
    """Get cached MDF object or create new one."""
    cache_key = f"{file_path}_{file_id}"

    if cache_key not in _mdf_cache:
        print(f"Loading MDF file into cache: {file_path}", flush=True)
        _mdf_cache[cache_key] = asammdf.MDF(file_path)

    return _mdf_cache[cache_key]

def clear_mdf_cache():
    """Clear MDF cache and close all files."""
    for mdf in _mdf_cache.values():
        try:
            mdf.close()
        except:
            pass
    _mdf_cache.clear()

def plot_signal(file_path, signal_name, current_figure=None, file_id=None):
    """Load MDF file and plot the specified signal with caching."""
    try:
        # Use cached MDF file
        mdf = get_cached_mdf(file_path, file_id or "default")

        print(f"Loading signal: {signal_name}", flush=True)

        # Get the signal data - this is the expensive operation
        signal_data = mdf.get(signal_name)

        if signal_data is None:
            raise ValueError(f"Signal '{signal_name}' not found")

        if len(signal_data.samples) == 0:
            raise ValueError(f"Signal '{signal_name}' has no data")

        # Extract time and values
        timestamps = signal_data.timestamps
        values = signal_data.samples

        print(f"Signal loaded: {len(timestamps)} data points", flush=True)

        # Create new figure or update existing one
        if current_figure is None or 'data' not in current_figure:
            fig = go.Figure()
        else:
            fig = go.Figure(current_figure)

        # Add new trace
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=values,
            mode='lines',
            name=signal_name,
            line=dict(width=1.5)
        ))

        # Update layout
        fig.update_layout(
            title=f"Signal Plot: {signal_name}",
            xaxis_title="Time (s)",
            yaxis_title="Value",
            template="plotly_white",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    except Exception as e:
        print(f"Error plotting signal {signal_name}: {e}", flush=True)
        # Return error figure
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"Error loading signal: {signal_name}",
            xaxis_title="Time (s)",
            yaxis_title="Value",
            template="plotly_white",
            annotations=[
                dict(
                    text=f"Error: {str(e)}",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="red")
                )
            ]
        )
        return error_fig