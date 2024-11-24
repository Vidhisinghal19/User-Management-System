# app/admin_routes.py

from flask import Blueprint, request, jsonify , render_template
from admin_operations import (
    create_role, create_department, create_user, read_users, update_user, delete_user
)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_portal():
    return render_template('admin_portal.html')

# Route to create a new user
@admin_bp.route('/create_user', methods=['POST'])
def admin_create_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

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

# Route to update an existing user
@admin_bp.route('/update_user/<int:user_id>', methods=['PUT'])
def update_existing_user(user_id):
    try:
        data = request.get_json()
        field = data['field']  # e.g., "user_name", "email_id"
        value = data['value']  # new value for the field

        # Call the update_user function with user_id, field, and value
        update_user(user_id, field, value)
        return jsonify({'message': f'User {user_id} updated successfully'}), 200
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete the user 
@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    try:
        delete_user(user_id)
        return jsonify({'message': f'User {user_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all users
@admin_bp.route('/users', methods=['GET'])
def admin_get_users():
    try:
        users = read_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new role
@admin_bp.route('/create_role', methods=['POST'])
def admin_create_role():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        data = request.get_json()
        role_name = data['role_name']
        create_role(role_name)
        return jsonify({'message': f"Role '{role_name}' created successfully"}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new department
@admin_bp.route('/create_department', methods=['POST'])
def admin_create_department():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    try:
        data = request.get_json()
        department_name = data['department_name']
        create_department(department_name)
        return jsonify({'message': f"Department '{department_name}' created successfully"}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
