from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # Allow frontend to call backend

# Database connection details (update with yours)
endpoint = 'database-1.cojyimmwa5y5.us-east-1.rds.amazonaws.com'
port = 3306
db_name = 'db1'
username = 'admin'
password = 'ugdqwq237e8yuhs'

def get_connection():
    return pymysql.connect(
        host=endpoint,
        port=port,
        user=username,
        password=password,
        db=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

# Create table if not exists
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender ENUM('male','female') NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/create", methods=["POST"])
def create_user():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age, gender) VALUES (%s, %s, %s)",
                   (data["name"], data["age"], data["gender"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created!"})

@app.route("/read", methods=["GET"])
def read_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/update", methods=["POST"])
def update_user():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET age=%s, gender=%s WHERE name=%s",
                   (data["age"], data["gender"], data["name"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "User updated!"})

@app.route("/delete", methods=["POST"])
def delete_user():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE name=%s", (data["name"],))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted!"})

if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000, debug=True)
