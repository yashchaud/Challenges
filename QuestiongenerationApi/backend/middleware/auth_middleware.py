from functools import wraps
from flask import request, jsonify, g
from backend.utils.helpers import decode_token
from backend.models.user import get_user_by_id

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1] 
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401



        if not token:
            return jsonify({'error': 'Token missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

       
        user = get_user_by_id(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401

       
        g.current_user = user
        return f(*args, **kwargs)

    return wrapper