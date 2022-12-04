from flask import Flask
from src.auth import auth
from src.token import token
from src.admin import admin
from src.modules.mongedb import mongo



def create_app():
    app = Flask(__name__,template_folder='../templates',static_folder='../static')
    app.secret_key = 'super secret key'
    app.config["JWT_SECRET_KEY"] = 'secret_key'

    app.register_blueprint(admin)
    app.register_blueprint(token)
    app.register_blueprint(auth)
    return app


