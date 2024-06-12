from flask import Flask
from flask_cors import CORS
import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    CORS(app)

    from .routes import main
    app.register_blueprint(main)

    return app
