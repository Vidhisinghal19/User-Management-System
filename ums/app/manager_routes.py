#app/manager_routes.py

from flask import Blueprint, request, jsonify, render_template
from db import get_connection
from manager_operations import (
    get_users_in_department,
    add_user,
    update_user,
    delete_user,
)

# Create a Blueprint for manager routes
manager_blueprint = Blueprint('manager_blueprint', __name__, url_prefix='/manager')

@manager_blueprint.route('/')
def manager_portal():
    return render_template('manager_portal.html')

@manager_blueprint.route('/login', methods=['POST'])
def manager_login():
    data = request.json
    email_id = data.get('email_id')
    passcode = data.get('passcode')

    if not email_id or not passcode:
        return jsonify({"error": "Email and passcode are required."}), 400

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT user_id, user_name, department_id 
            FROM users 
            WHERE email_id = %s AND passcode = %s AND role_id = 2  -- Role ID 2 for manager
        """, (email_id, passcode))
        
        manager = cursor.fetchone()

        if manager is None:
            return jsonify({"error": "Invalid email or passcode."}), 401

        user_id, user_name, department_id = manager
        # Store department_id in session or use it in the response
        return jsonify({
            "success": True,
            "message": "Login successful.",
            "user_id": user_id,
            "user_name": user_name,
            "department_id": department_id
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error during login: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@manager_blueprint.route('/users', methods=['GET'])
def list_users():
    department_id = request.args.get('department_id')
    
    if department_id is None:
        return jsonify({"error": "Department ID is required."}), 400
    
    # Fetch users only within the manager's department
    users = get_users_in_department(department_id)
    
    return jsonify(users), 200

#create user
@manager_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_name = data.get('user_name')
    email_id = data.get('email_id')
    passcode = data.get('passcode')
    manager_email = data.get('manager_email')  # Get manager email from request data
    logged_in_department_id = data.get('department_id')  # Get department ID from request data

    if not user_name or not email_id or not passcode or not manager_email or not logged_in_department_id:
        return jsonify({"error": "All fields are required."}), 400

    # Check for existing user
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email_id = %s", (email_id,))
        if cursor.fetchone():
            return jsonify({"error": "User with this email already exists."}), 409  # Conflict

        # Now we call add_user with the manager's email
        if add_user(manager_email, user_name, email_id, passcode):
            return jsonify({"success": True, "message": "User added successfully."}), 201
        else:
            return jsonify({"error": "Error adding user."}), 500
    except Exception as e:
        return jsonify({"error": f"Error adding user: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

#update user 
# update user
@manager_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json
    user_name = data.get('user_name')
    email_id = data.get('email_id')
    passcode = data.get('passcode')

    # Retrieve the department ID of the logged-in manager
    logged_in_department_id = data.get('department_id')  # Get department ID from request body

    if not user_name or not email_id or not passcode or not logged_in_department_id:
        return jsonify({"error": "All fields are required."}), 400

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            # Fetch the department of the user to be updated
            cursor.execute("SELECT department_id FROM users WHERE user_id = %s", (user_id,))
            user_department = cursor.fetchone()

            if user_department is None:
                return jsonify({"error": "User not found."}), 404

            user_department_id = user_department[0]

            # Ensure that logged_in_department_id is converted to an integer for comparison
            logged_in_department_id = int(logged_in_department_id)

            if user_department_id != logged_in_department_id:
                return jsonify({"error": "Cannot update user from a different department."}), 403

            # Call update_user function to update the user
            if update_user(user_id, user_name, email_id, passcode, logged_in_department_id):
                return jsonify({"success": True, "message": "User updated successfully."}), 200
            else:
                return jsonify({"error": "Error updating user."}), 500

    except Exception as e:
        return jsonify({"error": f"Error updating user: {e}"}), 500
    finally:
        connection.close()


@manager_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({"error": "User not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Error checking user existence: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

    # Proceed with the delete operation
    if delete_user(user_id):
        return jsonify({"success": True, "message": "User deleted successfully."}), 200
    else:
        return jsonify({"error": "Error deleting user."}), 500
