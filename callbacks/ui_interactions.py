"""
UI interaction callbacks including draggable divider functionality.
"""

from dash import Input, Output


def register_ui_callbacks(app):
    """Register UI interaction callbacks."""

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