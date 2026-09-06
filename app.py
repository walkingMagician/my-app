from flask import Flask, jsonify, request
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'db'),
                user=os.getenv('DB_USER', 'user'),
                password=os.getenv('DB_PASSWORD', 'password'),
                database=os.getenv('DB_NAME', 'appdb')
            )
            return conn
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            retries -= 1
            time.sleep(5)
    return None

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from My App!',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify({
        'users': [{'id': u[0], 'name': u[1], 'email': u[2]} for u in users]
    })

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and email required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email) VALUES (%s, %s)',
        (data['name'], data['email'])
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({
        'id': user_id,
        'name': data['name'],
        'email': data['email']
    }), 201

def init_db():
    conn = get_db_connection()
    if not conn:
        print("Не удалось инициализировать БД")
        return
    
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("База данных инициализирована")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)