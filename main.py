"""Main entry point for the Flask application."""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
