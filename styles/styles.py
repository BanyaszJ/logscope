"""
Enhanced styling for the Dash application with signal interaction styles.
Contains all CSS styles as Python dictionaries.
"""

# Color scheme
COLORS = {
    'primary': '#007bff',
    'success': '#28a745',
    'background': '#f5f5f5',
    'white': 'white',
    'border': '#ddd',
    'border_light': '#ccc',
    'text': '#333',
    'text_muted': '#666',
    'input_bg': '#f8f9fa',
    'console_bg': '#1e1e1e',
    'console_text': '#d4d4d4',
    'output_bg': '#f8f9fa',
    'output_border': '#e9ecef',
    'signal_hover': '#e3f2fd',
    'signal_border_hover': '#1976d2'
}

# Main container styles
MAIN_CONTAINER = {
    'height': '100vh',
    'backgroundColor': COLORS['background'],
    'display': 'flex'
}

APP_CONTAINER = {
    'margin': '0',
    'padding': '0',
    'fontFamily': 'Arial, sans-serif',
    'color': COLORS['text']
}

# Panel styles
LEFT_PANEL = {
    'width': '48%',
    'padding': '20px',
    'height': '100vh',
    'display': 'flex',
    'flexDirection': 'column'
}

RIGHT_PANEL = {
    'width': '48%',
    'padding': '20px'
}

DIVIDER = {
    'width': '4px',
    'height': '100vh',
    'backgroundColor': COLORS['border'],
    'cursor': 'col-resize',
    'userSelect': 'none',
    'borderLeft': f'1px solid {COLORS["border_light"]}',
    'borderRight': f'1px solid {COLORS["border_light"]}'
}

# Section styles
SECTION_CONTAINER = {
    'padding': '15px',
    'border': f'1px solid {COLORS["border"]}',
    'borderRadius': '5px',
    'marginBottom': '15px',
    'backgroundColor': COLORS['white']
}

SECTION_HEADER = {
    'margin': '0 0 10px 0',
    'color': COLORS['text']
}

# File upload styles
FILE_UPLOAD_CONTAINER = {
    'width': '100%',
    'display': 'flex',
    'alignItems': 'center'
}

FILE_PATH_INPUT = {
    'width': '95%',
    'height': '30px',
    'marginRight': '10px',
    'padding': '6px',
    'border': f'1px solid {COLORS["border_light"]}',
    'borderRadius': '4px',
    'backgroundColor': COLORS['input_bg'],
    'cursor': 'default'
}

BROWSE_BUTTON = {
    'width': '25%',
    'height': '30px',
    'backgroundColor': COLORS['primary'],
    'color': COLORS['white'],
    'border': 'none',
    'borderRadius': '4px',
    'cursor': 'pointer'
}

# Enhanced data fields styles for signal list
DATA_FIELDS_CONTAINER = {
    'padding': '15px',
    'border': f'1px solid {COLORS["border"]}',
    'borderRadius': '5px',
    'marginBottom': '5px',
    'backgroundColor': COLORS['white'],
    'flex': '1',
    'display': 'flex',
    'flexDirection': 'column',
    'minHeight': '0'
}

# Signal list specific styles
SIGNAL_LIST_CONTAINER = {
    'height': '300px',
    'overflowY': 'auto',
    'border': f'1px solid {COLORS["border"]}',
    'borderRadius': '4px',
    'backgroundColor': COLORS['white'],
    'padding': '5px'
}

SIGNAL_ITEM = {
    'padding': '8px 12px',
    'margin': '2px 0',
    'backgroundColor': COLORS['input_bg'],
    'border': f'1px solid {COLORS["output_border"]}',
    'borderRadius': '4px',
    'cursor': 'pointer',
    'userSelect': 'none',
    'fontSize': '13px',
    'fontFamily': 'monospace',
    'transition': 'all 0.2s ease'
}

SIGNAL_ITEM_HOVER = {
    'backgroundColor': COLORS['signal_hover'],
    'borderColor': COLORS['signal_border_hover']
}

DATA_TEXTAREA = {
    'width': '100%',
    'height': '100%',
    'padding': '10px',
    'border': f'1px solid {COLORS["border_light"]}',
    'borderRadius': '4px',
    'resize': 'none',
    'fontFamily': 'monospace'
}

DATA_OUTPUT = {
    'marginTop': '10px',
    'fontSize': '12px',
    'color': COLORS['text_muted']
}

# Python console styles (enhanced for drag-drop)
PYTHON_CONSOLE_INPUT = {
    'width': '100%',
    'height': '120px',
    'padding': '10px',
    'border': f'1px solid {COLORS["border_light"]}',
    'borderRadius': '4px',
    'fontFamily': 'Consolas, Monaco, monospace',
    'fontSize': '12px',
    'backgroundColor': COLORS['console_bg'],
    'color': COLORS['console_text'],
    'resize': 'none'
}

EXECUTE_BUTTON = {
    'marginTop': '5px',
    'padding': '5px 15px',
    'backgroundColor': COLORS['success'],
    'color': COLORS['white'],
    'border': 'none',
    'borderRadius': '3px',
    'cursor': 'pointer',
    'fontSize': '12px'
}

PYTHON_OUTPUT = {
    'marginTop': '10px',
    'padding': '10px',
    'backgroundColor': COLORS['output_bg'],
    'border': f'1px solid {COLORS["output_border"]}',
    'borderRadius': '4px',
    'fontFamily': 'Consolas, Monaco, monospace',
    'fontSize': '12px',
    'minHeight': '40px',
    'whiteSpace': 'pre-wrap'
}

# Visualization styles (enhanced for drag-drop)
PLOT_STYLE = {
    'height': '90vh'
}

# Drop zone styles
DROP_ZONE_ACTIVE = {
    'backgroundColor': 'rgba(25, 118, 210, 0.1)',
    'border': '2px dashed #1976d2'
}

DROP_ZONE_CONSOLE_ACTIVE = {
    'backgroundColor': 'rgba(40, 167, 69, 0.1)',
    'border': '2px dashed #28a745'
}
