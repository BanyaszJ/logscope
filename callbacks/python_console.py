"""
Python console callbacks for executing Python commands.
"""

import sys
import subprocess
import re
from io import StringIO
import traceback
from dash import Input, Output, State


# Global namespace to persist variables between executions
console_namespace = {}


def register_console_callbacks(app):
    """Register Python console callbacks."""

    @app.callback(
        [Output('python-output', 'children'),
         Output('python-context-store', 'data'),
         Output('python-variables', 'children')],
        [Input('execute-python-btn', 'n_clicks'),
         Input('clear-python-btn', 'n_clicks')],
        [State('python-cmd-input', 'value'),
         State('python-context-store', 'data')]
    )
    def execute_python_command(execute_clicks, clear_clicks, command, context_data):
        """Execute Python command and return output."""
        from dash import callback_context

        # Check which button was clicked
        if not callback_context.triggered:
            return "Output will appear here...", {}, "Variables: none"

        button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

        # Handle clear button
        if button_id == 'clear-python-btn' and clear_clicks:
            console_namespace.clear()
            return "Console cleared.", {}, "Variables: none"

        # Handle execute button
        if button_id != 'execute-python-btn' or not execute_clicks or not command:
            variables_display = format_variables_display(context_data or {})
            return "Output will appear here...", context_data or {}, variables_display

        # Check if command is a pip install
        if command.strip().startswith('!pip ') or command.strip().startswith('pip '):
            return handle_pip_command(command, context_data)

        # Update global namespace with any stored context
        if context_data:
            console_namespace.update(context_data)

        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = mystdout = StringIO()
        sys.stderr = mystderr = StringIO()

        output_text = ""

        try:
            # Execute the command in the persistent namespace
            exec(command, {"__builtins__": __builtins__}, console_namespace)

            # Get any printed output
            stdout_value = mystdout.getvalue()
            stderr_value = mystderr.getvalue()

            if stdout_value:
                output_text += stdout_value
            if stderr_value:
                output_text += stderr_value

            # If no output was printed, try to evaluate as expression
            if not output_text.strip():
                try:
                    result = eval(command, {"__builtins__": __builtins__}, console_namespace)
                    if result is not None:
                        output_text = str(result)
                except:
                    # If eval fails and no output, show success message
                    output_text = "Command executed successfully (no output)"

        except Exception as e:
            # Capture any errors
            output_text = f"Error: {str(e)}\n{traceback.format_exc()}"

        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        # Store variables that can be serialized (basic types only)
        storable_context = {}
        for key, value in console_namespace.items():
            if not key.startswith('_'):  # Skip private variables
                try:
                    # Try to store only serializable types
                    if isinstance(value, (int, float, str, bool, list, dict, type(None))):
                        storable_context[key] = value
                    elif hasattr(value, '__name__'):  # Functions, classes
                        storable_context[key] = f"<{type(value).__name__}: {value.__name__}>"
                    else:
                        storable_context[key] = f"<{type(value).__name__} object>"
                except:
                    continue

        variables_display = format_variables_display(storable_context)
        return output_text or "Command executed successfully (no output)", storable_context, variables_display


def handle_pip_command(command, context_data):
    """Handle pip install commands."""
    try:
        # Clean the command - remove ! if present and ensure proper format
        clean_command = command.strip()
        if clean_command.startswith('!'):
            clean_command = clean_command[1:]

        # Split into parts for subprocess
        cmd_parts = clean_command.split()

        # Run pip command
        result = subprocess.run(
            [sys.executable, '-m'] + cmd_parts,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\n" + result.stderr

        if result.returncode == 0:
            output += f"\n✓ Package installation completed successfully!"
        else:
            output += f"\n✗ Installation failed (return code: {result.returncode})"

        variables_display = format_variables_display(context_data or {})
        return output, context_data or {}, variables_display

    except subprocess.TimeoutExpired:
        variables_display = format_variables_display(context_data or {})
        return "Error: Pip command timed out (60s limit)", context_data or {}, variables_display
    except Exception as e:
        variables_display = format_variables_display(context_data or {})
        return f"Error executing pip command: {str(e)}", context_data or {}, variables_display


def format_variables_display(variables):
    """Format variables for display in the variables panel."""
    if not variables:
        return "Variables: none"

    var_strings = []
    for key, value in variables.items():
        if isinstance(value, str) and len(value) > 30:
            value_str = f'"{value[:27]}..."'
        elif isinstance(value, list) and len(value) > 5:
            value_str = f"[{', '.join(map(str, value[:3]))}, ...] (len={len(value)})"
        else:
            value_str = str(value)
        var_strings.append(f"{key} = {value_str}")

    return "Variables: " + ", ".join(var_strings)