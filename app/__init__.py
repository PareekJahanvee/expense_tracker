from flask import Flask

def create_app():
    app = Flask(__name__)

    # Ensure the app is configured to serve static files
    app.config['STATIC_FOLDER'] = 'static'

    # Import routes
    from . import routes

    # Register routes
    app.register_blueprint(routes.routes)

    return app
