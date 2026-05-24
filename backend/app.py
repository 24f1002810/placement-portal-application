from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from models import db, User, Role
from models import *
from config import LocalDevelopmentConfig
from datetime import datetime

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

app = None
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    app.config['SECRET_KEY'] = 'super-secret-key-change-in-prod'
    app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt'
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False # Essential for pure API token auth
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['SECURITY_SESSION_PROTECTION'] = 'strong'

    db.init_app(app)
    security = Security(app, user_datastore)
    app.app_context().push()
    # Enable CORS for all routes
    CORS(app, 
         origins="*",
         allow_headers=["Content-Type", "Authentication-Token"],
         supports_credentials=True)
    return app

app = create_app()

from routes import *

if __name__ == "__main__":
    db.create_all()
    app.run()