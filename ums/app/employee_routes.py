#app/employee_routes.py

from flask import Blueprint, request, jsonify, render_template
from employee_operations import get_employee_profile, update_employee_profile
from db import get_connection

employee_bp = Blueprint('employee', __name__)

# Employee Portal
@employee_bp.route('/')
def employee_portal():
    return render_template('employee_portal.html')

# Login
@employee_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    # Check if data exists and has the required fields
    if not data or 'email_id' not in data or 'passcode' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    email_id = data.get('email_id')
    passcode = data.get('passcode')

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Verify the employee's email and passcode
        cursor.execute("SELECT user_id FROM users WHERE email_id = %s AND passcode = %s", (email_id, passcode))
        employee = cursor.fetchone()
        
        if employee:
            return jsonify({'message': 'Login successful', 'user_id': employee['user_id']}), 200
        return jsonify({'message': 'Invalid email or passcode'}), 401

    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

# View Employee Profile
@employee_bp.route('/profile/<int:user_id>', methods=['GET'])
def view_profile(user_id):
    return get_employee_profile(user_id)

# Modify Employee Profile
@employee_bp.route('/profile/<int:user_id>', methods=['PUT'])
def modify_profile(user_id):
    data = request.json
    
    # Ensure that the data is valid and has required fields
    if not data or 'user_name' not in data or 'email_id' not in data:
        return jsonify({'message': 'Invalid input data'}), 400
    
    return update_employee_profile(user_id, data)
