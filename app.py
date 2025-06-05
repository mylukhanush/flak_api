from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # MySQL host
            user="root",       # Your MySQL username
            password="Bunny@1806",  # Your MySQL password
            database="flask_crud"  # Your database name
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route to fetch all users (GET method)
@app.route('/users', methods=['GET'])
def get_users():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees")
        users = cursor.fetchall()
        connection.close()
        return jsonify(users)  # Returns a list of users in JSON format
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Route to add a new user (POST method)
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    id = data.get('id')
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO employees (id,name, email) VALUES (%s, %s,%s)", (id,name, email))
            connection.commit()
            connection.close()
            return jsonify({"message": "User added successfully"}), 201
        except Error as e:
            connection.close()
            return jsonify({"error": f"Error inserting user: {e}"}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Route to fetch a single user by ID (GET method)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        connection.close()
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Route to update a user (PUT method)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        connection.commit()
        connection.close()
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

# Route to delete a user (DELETE method)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        connection.commit()
        connection.close()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)