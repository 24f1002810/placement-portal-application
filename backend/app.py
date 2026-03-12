from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from models import *
from config import LocalDevelopmentConfig
from datetime import datetime

app = None
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    CORS(app)
    return app

app = create_app()

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    # Validate credentials here
    return jsonify({"message": "Login successful"})

if __name__ == "__main__":
    db.create_all()
    if not Admin.query.first():
        db.session.add(Admin(password = 'admin123'))
        db.session.commit()
    app.run()