from flask import Blueprint, request, jsonify, g
from backend.models.user import create_user, get_user_by_email
from backend.utils.helpers import hash_password, check_password, generate_token
from backend.middleware.auth_middleware import require_auth

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    email = data['email'].lower().strip()
    password = data['password']

   
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

   
    password_hash = hash_password(password)
    user = create_user(email, password_hash)

    if not user:
        return jsonify({'error': 'Failed to create user - database may be down'}), 500

    return jsonify({
        'message': 'User created successfully',
        'user': {'id': user['id'], 'email': user['email']}
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    email = data['email'].lower().strip()
    password = data['password']

    
    user = get_user_by_email(email)
    if not user or not check_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401

   
    token = generate_token(user['id'])

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {'id': user['id'], 'email': user['email']}
    })

@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    return jsonify({
        'user': {
            'id': g.current_user['id'],
            'email': g.current_user['email']
        }
    })