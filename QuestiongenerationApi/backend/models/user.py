import mysql.connector
from backend.utils.database import get_db_connection

def create_user(email, password_hash):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid

            user = {
                'id': user_id,
                'email': email,
                'password_hash': password_hash
            }
            return user

        except mysql.connector.IntegrityError:
            return None
        finally:
            cursor.close()
            conn.close()
    except Exception:
        return None

def get_user_by_email(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user
    except Exception:
        return None

def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        return user
    except Exception:
        return None