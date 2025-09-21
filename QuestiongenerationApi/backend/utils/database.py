import mysql.connector
from flask import current_app

def get_db_connection():
    conn = mysql.connector.connect(
        host=current_app.config['DB_HOST'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_NAME']
    )
    return conn

def init_db():
    try:
        conn = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {current_app.config['DB_NAME']}")
        cursor.close()
        conn.close()

       
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created successfully")
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("App will start but database features won't work")