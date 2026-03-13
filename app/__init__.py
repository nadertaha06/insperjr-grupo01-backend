from flask import Flask
from flask_cors import CORS


def create_app(config_name="development"):
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(f"config.{config_name.capitalize()}Config")

    from app.routes import register_routes
    register_routes(app)

    return app
