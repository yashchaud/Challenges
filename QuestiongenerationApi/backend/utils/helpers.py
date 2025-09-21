import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(user_id):
    expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])

    payload = {
        'user_id': user_id,
        'exp': expiry
    }

    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    return token

def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=[current_app.config['JWT_ALGORITHM']]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None