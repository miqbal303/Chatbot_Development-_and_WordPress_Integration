from flask import Flask
from app.config import configure_app
from app.routes import register_routes

def create_app():
    application = Flask(__name__)
    app = application
    configure_app(app)
    register_routes(app)
    return app
