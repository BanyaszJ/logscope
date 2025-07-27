import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
app = dash.Dash(__name__)

# Custom CSS styling
app.layout = html.Div([
    # Main container with left and right sections
    html.Div([
        # Left panel
        html.Div([
            # Top section with file browser
            html.Div([
                # Combined file path input and drag-drop area
                dcc.Upload(
                    id='file-upload-area',
                    children=[
                        dcc.Input(
                            id='file-path-input',
                            type='text',
                            placeholder='Enter file path or drag & drop files here...',
                            disabled=True,
                            style={
                                'width': '70%',
                                'height': '30px',
                                'marginRight': '10px',
                                'padding': '6px',
                                'border': '1px solid #ccc',
                                'borderRadius': '4px',
                                'backgroundColor': '#f8f9fa',
                                'cursor': 'default'
                            }
                        ),
                        # Browse button
                        html.Button(
                            'Browse',
                            id='browse-button',
                            style={
                                'width': '25%',
                                'height': '30px',
                                'backgroundColor': '#007bff',
                                'color': 'white',
                                'border': 'none',
                                'borderRadius': '4px',
                                'cursor': 'pointer'
                            }
                        )
                    ],
                    style={
                        'width': '100%',
                        'display': 'flex',
                        'alignItems': 'center'
                    },
                    multiple=True
                )
            ], style={
                'padding': '15px',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'marginBottom': '15px',
                'backgroundColor': 'white'
            }),

            # Middle section - Data Fields (fills remaining space)
            html.Div([
                html.H4("Data Fields", style={'margin': '0 0 10px 0', 'color': '#333'}),
                dcc.Textarea(
                    id='string-list-field',
                    placeholder='Field 1\nField 2\nField 3',
                    style={
                        'width': '100%',
                        'height': '100%',
                        'padding': '10px',
                        'border': '1px solid #ccc',
                        'borderRadius': '4px',
                        'resize': 'none',
                        'fontFamily': 'monospace'
                    }
                ),
                html.Div(
                    id='string-list-output',
                    style={'marginTop': '10px', 'fontSize': '12px', 'color': '#666'}
                )
            ], style={
                'padding': '15px',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'marginBottom': '15px',
                'backgroundColor': 'white',
                'flex': '1',
                'display': 'flex',
                'flexDirection': 'column',
                'minHeight': '0'
            }),

            # Bottom section - Python Console (fixed at bottom)
            html.Div([
                html.H4("Python Console", style={'margin': '0 0 10px 0', 'color': '#333'}),
                html.Div([
                    dcc.Textarea(
                        id='python-cmd-input',
                        placeholder='>>> Enter Python commands here...\n# Example:\n# print("Hello World")\n# x = [1, 2, 3, 4]\n# sum(x)',
                        style={
                            'width': '100%',
                            'height': '120px',
                            'padding': '10px',
                            'border': '1px solid #ccc',
                            'borderRadius': '4px',
                            'fontFamily': 'Consolas, Monaco, monospace',
                            'fontSize': '12px',
                            'backgroundColor': '#1e1e1e',
                            'color': '#d4d4d4',
                            'resize': 'none'
                        }
                    ),
                    html.Button(
                        'Execute',
                        id='execute-python-btn',
                        style={
                            'marginTop': '5px',
                            'padding': '5px 15px',
                            'backgroundColor': '#28a745',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '3px',
                            'cursor': 'pointer',
                            'fontSize': '12px'
                        }
                    )
                ]),
                html.Div(
                    id='python-output',
                    style={
                        'marginTop': '10px',
                        'padding': '10px',
                        'backgroundColor': '#f8f9fa',
                        'border': '1px solid #e9ecef',
                        'borderRadius': '4px',
                        'fontFamily': 'Consolas, Monaco, monospace',
                        'fontSize': '12px',
                        'minHeight': '40px',
                        'whiteSpace': 'pre-wrap'
                    }
                )
            ], style={
                'padding': '15px',
                'border': '1px solid #ddd',
                'borderRadius': '5px',
                'backgroundColor': 'white'
            })

        ], style={
            'width': '48%',
            'padding': '20px',
            'height': '100vh',
            'display': 'flex',
            'flexDirection': 'column'
        }, id='left-panel'),

        # Draggable divider
        html.Div(
            id='divider',
            style={
                'width': '4px',
                'height': '100vh',
                'backgroundColor': '#ddd',
                'cursor': 'col-resize',
                'userSelect': 'none',
                'borderLeft': '1px solid #ccc',
                'borderRight': '1px solid #ccc'
            }
        ),


        html.Div([
            html.H4("Data Visualization", style={'margin': '0 0 15px 0', 'color': '#333'}),
            dcc.Graph(
                id='main-plot',
                style={'height': '90vh'},
                figure=go.Figure().update_layout(
                    title="Ready for Data",
                    xaxis_title="X Axis",
                    yaxis_title="Y Axis",
                    template="plotly_white",
                    annotations=[
                        dict(
                            text="Load data to display plots here",
                            x=0.5,
                            y=0.5,
                            xref="paper",
                            yref="paper",
                            showarrow=False,
                            font=dict(size=20, color="gray")
                        )
                    ]
                )
            )
        ], style={
            'width': '48%',
            'padding': '20px'
        }, id='right-panel')

    ], style={'height': '100vh', 'backgroundColor': '#f5f5f5', 'display': 'flex'}),

    # Hidden stores for data
    dcc.Store(id='uploaded-files-store'),
    dcc.Store(id='string-list-store'),
    dcc.Store(id='python-context-store')
], style={'margin': '0', 'padding': '0', 'fontFamily': 'Arial, sans-serif', 'color': '#333'})

# Clientside callback for draggable divider
app.clientside_callback(
    """
    function(n_clicks) {
        let isDragging = false;
        let startX = 0;
        let startLeftWidth = 0;
        let startRightWidth = 0;
        
        const divider = document.getElementById('divider');
        const leftPanel = document.getElementById('left-panel');
        const rightPanel = document.getElementById('right-panel');
        const container = divider.parentElement;
        
        if (!divider || !leftPanel || !rightPanel) return window.dash_clientside.no_update;
        
        function onMouseDown(e) {
            isDragging = true;
            startX = e.clientX;
            
            // Get current widths as percentages
            const containerWidth = container.offsetWidth;
            startLeftWidth = (leftPanel.offsetWidth / containerWidth) * 100;
            startRightWidth = (rightPanel.offsetWidth / containerWidth) * 100;
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
            e.preventDefault();
        }
        
        function onMouseMove(e) {
            if (!isDragging) return;
            
            const deltaX = e.clientX - startX;
            const containerWidth = container.offsetWidth;
            const deltaPercent = (deltaX / containerWidth) * 100;
            
            let newLeftWidth = startLeftWidth + deltaPercent;
            let newRightWidth = startRightWidth - deltaPercent;
            
            // Set minimum widths (20% and 20%)
            if (newLeftWidth < 20) {
                newLeftWidth = 20;
                newRightWidth = 76; // 100 - 20 - 4 (divider)
            }
            if (newRightWidth < 20) {
                newRightWidth = 20;
                newLeftWidth = 76; // 100 - 20 - 4 (divider)
            }
            
            leftPanel.style.width = newLeftWidth + '%';
            rightPanel.style.width = newRightWidth + '%';
        }
        
        function onMouseUp() {
            isDragging = false;
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }
        
        // Remove existing listeners to prevent duplicates
        divider.removeEventListener('mousedown', onMouseDown);
        // Add the mousedown listener
        divider.addEventListener('mousedown', onMouseDown);
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('divider', 'style'),
    Input('divider', 'id')
)

# Callback for file upload
@app.callback(
    [Output('uploaded-files-store', 'data'),
     Output('file-path-input', 'value')],
    [Input('file-upload-area', 'contents')],
    [State('file-upload-area', 'filename')]
)
def handle_file_upload(contents, filenames):
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

# Callback for string list processing
@app.callback(
    [Output('string-list-store', 'data'),
     Output('string-list-output', 'children')],
    [Input('string-list-field', 'value')]
)
def process_string_list(text_input):
    if not text_input:
        return [], "No items entered"

    # Split by lines and clean up
    string_list = [line.strip() for line in text_input.split('\n') if line.strip()]

    return string_list, f"Items: {len(string_list)} | Preview: {', '.join(string_list[:3])}{'...' if len(string_list) > 3 else ''}"

# Callback for Python console (placeholder for now)
@app.callback(
    Output('python-output', 'children'),
    [Input('execute-python-btn', 'n_clicks')],
    [State('python-cmd-input', 'value')]
)
def execute_python_command(n_clicks, command):
    if not n_clicks or not command:
        return "Output will appear here..."

    # Placeholder - will be extended later
    return f"Command received:\n{command}\n\n[Python execution will be implemented later]"

# Callback for browse button (placeholder)
@app.callback(
    Output('file-path-input', 'placeholder'),
    [Input('browse-button', 'n_clicks')]
)
def handle_browse_click(n_clicks):
    if n_clicks:
        return "Browse functionality will be implemented..."
    return 'Enter file path or drag & drop files here...'

if __name__ == '__main__':
    app.run(debug=True)