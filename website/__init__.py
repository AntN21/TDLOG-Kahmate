"""
Web application initialization file
"""
from flask import Flask
from flask_socketio import SocketIO

SOCKET = None

def create_app():
    """ Creates the app to be used and initiates its socket"""

    app = Flask(__name__)
    app.config["SECRET_KEY"] = ""
    global SOCKET
    SOCKET = SocketIO(app, cors_allowed_origins="*")

    from .views import views

    app.register_blueprint(views, url_prefix="/")
    return app


def run_app(app):
    """Starts the game application via its socket"""

    SOCKET.run(app, debug=True)
