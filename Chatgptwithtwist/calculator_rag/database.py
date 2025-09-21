import mysql.connector
import json
from datetime import datetime
import subprocess
from config import MYSQL_CONFIG


def check_mysql_service():
    service_names = ['mysql', 'mysql80', 'mysql57', 'wampmysqld64', 'mysqld']

    for service_name in service_names:
        try:
            result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True)
            if 'RUNNING' in result.stdout:
                print(f"Found MySQL service '{service_name}' running")
                return True
        except:
            continue

    print("MySQL service detection failed - will test connection directly")
    return None


def test_mysql_connection():
    try:
        print("Testing MySQL connection...")
        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            port=MYSQL_CONFIG['port'],
            charset=MYSQL_CONFIG['charset']
        )
        connection.close()
        print("MySQL connection successful!")
        return True
    except mysql.connector.Error as e:
        print(f"MySQL connection failed: {e}")
        return False


def setup_database():
    service_status = check_mysql_service()

    if service_status is False:
        print("MySQL service not running. Please start MySQL service.")
        return False

    if not test_mysql_connection():
        if service_status is None:
            print("Could not detect MySQL service, but connection test failed.")
            print("Please ensure MySQL is running and check credentials in config.py")
        else:
            print("\nPlease update your MySQL credentials in config.py")
        return False

    try:
        print(f"Setting up database '{MYSQL_CONFIG['database']}'...")

        connection = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            port=MYSQL_CONFIG['port'],
            charset=MYSQL_CONFIG['charset']
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
        cursor.execute(f"USE {MYSQL_CONFIG['database']}")

        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS calculations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            query TEXT NOT NULL,
            operation VARCHAR(50),
            result DOUBLE,
            expression TEXT,
            embedding JSON,
            user VARCHAR(100) DEFAULT 'system',
            tags JSON,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user (user),
            INDEX idx_timestamp (timestamp),
            INDEX idx_operation (operation)
        )
        """

        cursor.execute(create_tables_sql)
        connection.commit()
        cursor.close()
        connection.close()
        print("MySQL database initialized successfully!")
        return True

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        print("Please check your MySQL credentials in config.py")
        print("Common issues:")
        print("- Wrong username/password")
        print("- MySQL server not running")
        print("- Wrong port number")
        print("- Access denied for user")
        return False
    except Exception as e:
        print(f"Database setup failed: {e}")
        return False


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        database=MYSQL_CONFIG['database'],
        port=MYSQL_CONFIG['port'],
        charset=MYSQL_CONFIG['charset']
    )


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()
        return result

    except Exception as e:
        print(f"Database error: {e}")
        return None


# Global model cache
_model_cache = None

def get_embedding_model():
    global _model_cache
    if _model_cache is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("Loading sentence-transformer model (first time may take a moment)...")
            _model_cache = SentenceTransformer('all-MiniLM-L6-v2')
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Failed to load sentence-transformer: {e}")
            _model_cache = False
    return _model_cache

def get_embedding(text):
    model = get_embedding_model()
    if model:
        try:
            return model.encode(text).tolist()
        except:
            pass

    # Fallback to simple hash-based embedding
    words = text.lower().split()
    return [hash(word) % 1000 for word in words[:10]] + [0] * (10 - min(len(words), 10))


def calculate_similarity(embedding1, embedding2):
    try:
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        return cosine_similarity([embedding1], [embedding2])[0][0]
    except:
        return 0.5 if embedding1 == embedding2 else 0.1


FAST_MODE = True  # Set to False for full embeddings

def store_calculation(query, operation, result, user="system"):
    if FAST_MODE:
        # Skip embedding calculation for faster responses
        embedding = []
    else:
        embedding = get_embedding(query)

    tags = []
    query_lower = query.lower()
    if any(word in query_lower for word in ['rice', 'food', 'kg']):
        tags.append('food')
    if any(word in query_lower for word in ['rent', 'money', 'bill']):
        tags.append('money')

    insert_query = """
    INSERT INTO calculations (query, operation, result, expression, embedding, user, tags, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (query, operation, result, query, json.dumps(embedding), user, json.dumps(tags), datetime.now())
    return execute_query(insert_query, params)


def get_calculations(limit=100, user=None):
    if user:
        query = "SELECT * FROM calculations WHERE user = %s ORDER BY timestamp DESC LIMIT %s"
        return execute_query(query, (user, limit), fetch_all=True) or []
    else:
        query = "SELECT * FROM calculations ORDER BY timestamp DESC LIMIT %s"
        return execute_query(query, (limit,), fetch_all=True) or []


def search_calculations(search_text, limit=10):
    search_embedding = get_embedding(search_text)
    all_calcs = get_calculations(1000)

    if not all_calcs:
        return []

    scored_calcs = []
    for calc in all_calcs:
        try:
            calc_embedding = json.loads(calc['embedding'])
            similarity = calculate_similarity(search_embedding, calc_embedding)
            scored_calcs.append((calc, similarity))
        except:
            continue

    scored_calcs.sort(key=lambda x: x[1], reverse=True)
    return [calc for calc, score in scored_calcs[:limit] if score > 0.1]


def delete_calculation(calc_id):
    query = "DELETE FROM calculations WHERE id = %s"
    return execute_query(query, (calc_id,))


def clear_all_calculations():
    query = "DELETE FROM calculations"
    return execute_query(query)