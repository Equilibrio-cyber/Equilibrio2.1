from flask import Flask
from .models import db  # AHORA SÍ FUNCIONA
from .routes import main

def create_app():
    app = Flask(__name__)
    app.secret_key = 'equilibrio_secreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equilibrio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main)

    return app
