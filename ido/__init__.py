import os
from flask import Flask

BASE_DIR = os.path.dirname(__file__)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from flask_cors import CORS
    CORS(app)

    from ido.models import db

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from ido.api import api
    app.register_blueprint(api)

    return app