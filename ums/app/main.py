from flask import Flask, request, jsonify
from db import get_connection
from models import create_tables, insert_initial_data
from admin_routes import admin_bp  # Import admin Blueprint
from manager_routes import manager_blueprint  # Import manager Blueprint
from employee_routes import employee_bp

from admin_operations import create_role, create_department, create_user, read_users, update_user, delete_user
import threading

# Initialize Flask app
app = Flask(__name__)

# Admin login route 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email_id = data.get('email_id')
    passcode = data.get('passcode')

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch admin data based on email and passcode
    cursor.execute("""
        SELECT * FROM users 
        WHERE email_id = %s 
        AND passcode = %s 
        AND role_id = (SELECT role_id FROM roles WHERE role_name = 'Administrator')
    """, (email_id, passcode))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if admin:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid email or passcode'}), 401

# Route to create a new user in the database 
@app.route('/create_user', methods=['POST'])
def create_new_user():
    try:
        data = request.get_json()
        user_name = data['user_name']
        role_id = data['role_id']
        department_id = data.get('department_id')  # This can be None
        email_id = data['email_id']
        passcode = data['passcode']
        create_user(user_name, role_id, department_id, email_id, passcode)
        return jsonify({'message': 'User created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update a user in the database 
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    try:
        data = request.get_json()

        # Instead of a single field, pass the entire dictionary for updating multiple fields
        fields = {key: value for key, value in data.items() if value is not None}

        if not fields:
            return jsonify({'error': 'At least one field must be provided'}), 400

        update_user(user_id, **fields)
        return jsonify({'message': f'User {user_id} updated successfully'}), 200
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a user in the database 
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_existing_user(user_id):
    try:
        delete_user(user_id)
        return jsonify({'message': f'User {user_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all users from the database 
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = read_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new role in the database 
@app.route('/create_role', methods=['POST'])
def create_new_role():
    try:
        data = request.get_json()
        role_name = data['role_name']
        create_role(role_name)
        return jsonify({'message': f"Role '{role_name}' created successfully"}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new department in the database 
@app.route('/create_department', methods=['POST'])
def create_new_department():
    try:
        data = request.get_json()
        department_name = data['department_name']
        create_department(department_name)
        return jsonify({'message': f"Department '{department_name}' created successfully"}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Register admin and manager Blueprints with appropriate prefixes
app.register_blueprint(admin_bp, url_prefix='/admin')  # All admin routes will be prefixed with /admin
app.register_blueprint(manager_blueprint, url_prefix='/manager')  # All manager routes will be prefixed with /manager
app.register_blueprint(employee_bp, url_prefix='/employee') #all employee routes
# Function to run Flask
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    
    # Start the Flask app in a thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
