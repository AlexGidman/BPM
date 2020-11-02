"""
BPM

A Flask web application for searching tempo and key signature information
using the Spotify API.

"""
import os

from flask import Flask, Blueprint

from .views import main


def create_app(test_config=None) -> Flask:
    """Create and configure the Flask app.
    
    Args: 
        test_config: test configuration file for running tests during development

    Returns:
        app (Flask): Flask application
    
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")

    app.register_blueprint(main)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    return app

