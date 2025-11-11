from flask import Blueprint, request, jsonify
from models.models import db, User, Patient
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg': 'Username already exists'}), 400

    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed_pw, role='Patient')
    db.session.add(user)
    db.session.commit()

    patient = Patient(user_id=user.id, contact_info=data.get('contact_info'), age=data.get('age'), gender=data.get('gender'))
    db.session.add(patient)
    db.session.commit()

    return jsonify({'msg': 'Patient registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'token': token, 'role': user.role}), 200