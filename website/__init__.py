from flask import Flask
from flask_socketio import SocketIO

socket = None


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = ""
    global socket
    socket = SocketIO(app, cors_allowed_origins="*")

    from .views import views

    app.register_blueprint(views, url_prefix="/")
    return app


def run_app(app):
    socket.run(app, debug=True)
