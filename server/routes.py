# routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Book, Order

api = Blueprint('api', __name__)

# User Registration
@api.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify(message="User already exists"), 400

    new_user = User(username=data['username'])
    new_user.set_password(data['password'])  # Hash password
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User created"), 201

# User Login
@api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):  # Validate password
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Bad credentials"), 401

# Get all books
@api.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': b.id, 'title': b.title, 'author': b.author, 'genre': b.genre, 'price': b.price} for b in books]), 200

# Add a new book (Admin only)
@api.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify(message="Admin only"), 403

    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], genre=data['genre'], price=data['price'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(message="Book added"), 201

# Add other routes as needed
