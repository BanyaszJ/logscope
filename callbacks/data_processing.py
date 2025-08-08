"""
Data processing callbacks for signal selection and plotting with ctrl+click support.
"""

import asammdf
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, ALL, callback_context, html
from dash.exceptions import PreventUpdate
from components.data_fields import create_signal_item, create_signal_item_with_state


def register_data_callbacks(app):
    """Register data processing callbacks."""

    # Update signal list when MDF file is loaded OR when plotted signals change
    @app.callback(
        [Output('signal-list-container', 'children'),
         Output('string-list-store', 'data'),
         Output('string-list-output', 'children')],
        [Input('uploaded-files-store', 'data'),
         Input('plotted-signals-store', 'data')]
    )
    def update_signal_list(files_data, plotted_signals):
        """Update the signal list display when MDF file is loaded or signals change."""
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
        plotted_signals = plotted_signals or []

        # Create interactive signal items with highlighting
        signal_items = []
        for i, signal_name in enumerate(signal_names):
            is_plotted = signal_name in plotted_signals
            signal_items.append(create_signal_item_with_state(signal_name, i, is_plotted))

        # Update summary
        summary = f"Signals: {len(signal_names)} loaded from {files_data.get('original_filename', 'MDF file')}"
        if plotted_signals:
            summary += f" | {len(plotted_signals)} plotted"

        return signal_items, signal_names, summary

    # Handle signal item clicks with ctrl+click support
    @app.callback(
        [Output('main-plot', 'figure'),
         Output('plotted-signals-store', 'data')],
        [Input({'type': 'signal-item', 'index': ALL}, 'n_clicks'),
         Input('clear-plot-btn', 'n_clicks')],
        [State('uploaded-files-store', 'data'),
         State('main-plot', 'figure'),
         State('plotted-signals-store', 'data')]
    )
    def handle_signal_click(n_clicks_list, clear_clicks, files_data, current_figure, plotted_signals):
        """Handle signal item clicks and clear button with ctrl+click support."""
        if not callback_context.triggered:
            raise PreventUpdate

        # Check what triggered the callback
        triggered_id = callback_context.triggered[0]['prop_id']

        # Handle clear button
        if 'clear-plot-btn' in triggered_id and clear_clicks:
            # Create empty plot
            empty_figure = create_signals_plot(None, [])
            return empty_figure, []

        # Handle signal clicks
        if not files_data or 'n_clicks' not in triggered_id:
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

        # Initialize plotted signals if None
        plotted_signals = plotted_signals or []

        # For now, implement toggle behavior (click to add/remove)
        # We'll enhance this with clientside ctrl detection later
        if signal_name in plotted_signals:
            # Remove signal
            new_plotted_signals = [s for s in plotted_signals if s != signal_name]
        else:
            # Add signal
            new_plotted_signals = plotted_signals + [signal_name]

        # Create the plot
        try:
            figure = create_signals_plot(file_path, new_plotted_signals, files_data.get('file_id'))
            return figure, new_plotted_signals
        except Exception as e:
            print(f"Error plotting signals: {e}")
            raise PreventUpdate

    # Remove the problematic clientside callback - we'll handle styling server-side

    # Clear cache when new file is loaded
    @app.callback(
        Output('placeholder', 'children'),  # Dummy output
        [Input('uploaded-files-store', 'data')]
    )
    def clear_cache_on_new_file(files_data):
        """Clear MDF cache when a new file is loaded."""
        if files_data and 'file_id' in files_data:
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

def create_signals_plot(file_path, signal_names, file_id=None):
    """Create a plot with multiple signals."""
    if not signal_names:
        # Return default empty figure
        fig = go.Figure()
        fig.update_layout(
            title="Ready for Data",
            xaxis_title="Time (s)",
            yaxis_title="Value",
            template="plotly_white",
            annotations=[
                dict(
                    text="Click signals to display plots here",
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=16, color="gray")
                )
            ]
        )
        return fig

    try:
        # Use cached MDF file
        mdf = get_cached_mdf(file_path, file_id or "default")

        # Create new figure
        fig = go.Figure()

        # Colors for different signals
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

        plotted_count = 0
        for i, signal_name in enumerate(signal_names):
            try:
                print(f"Loading signal: {signal_name}", flush=True)

                # Get the signal data
                signal_data = mdf.get(signal_name)

                if signal_data is None:
                    print(f"Signal '{signal_name}' not found", flush=True)
                    continue

                if len(signal_data.samples) == 0:
                    print(f"Signal '{signal_name}' has no data", flush=True)
                    continue

                # Add trace to plot
                fig.add_trace(go.Scatter(
                    x=signal_data.timestamps,
                    y=signal_data.samples,
                    mode='lines',
                    name=signal_name,
                    line=dict(color=colors[i % len(colors)], width=2)
                ))
                plotted_count += 1

            except Exception as e:
                print(f"Error plotting signal {signal_name}: {e}", flush=True)
                continue

        # Update layout
        if plotted_count > 0:
            title = f"Signal Plot ({plotted_count} signals)" if plotted_count > 1 else f"Signal Plot: {signal_names[0]}"
            fig.update_layout(
                title=title,
                xaxis_title="Time (s)",
                yaxis_title="Value",
                template="plotly_white",
                hovermode='x unified',
                legend=dict(
                    x=0.02,  # Position from left edge (2% from left)
                    y=0.98,  # Position from bottom (98% from bottom = top)
                    xanchor='left',
                    yanchor='top',
                    bgcolor='rgba(255, 255, 255, 0.8)',  # Semi-transparent white background
                    bordercolor='rgba(0, 0, 0, 0.2)',   # Light border
                    borderwidth=1,
                    font=dict(size=11)  # Slightly smaller font for compactness
                ),
                margin=dict(t=50, l=50, r=20, b=50)  # Reduced margins since legend is inside
            )
        else:
            fig.update_layout(
                title="No Valid Signals Found",
                template="plotly_white",
                annotations=[
                    dict(
                        text="Selected signals could not be plotted",
                        x=0.5,
                        y=0.5,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=16, color="orange")
                    )
                ]
            )

        return fig

    except Exception as e:
        print(f"Error creating signals plot: {e}", flush=True)
        # Return error figure
        fig = go.Figure()
        fig.update_layout(
            title="Error Loading Signals",
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
        return fig