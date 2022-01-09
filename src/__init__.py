from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

# instantiate the db
db = SQLAlchemy()


def create_app(script_info=None):
    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    # register blueprints
    from src.api.ping import ping_blueprint

    app.register_blueprint(ping_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
