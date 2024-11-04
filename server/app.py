# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
db.init_app(app)

jwt = JWTManager(app)  # Initialize the JWT manager

with app.app_context():
    db.create_all()  # Create tables if they don't exist

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
