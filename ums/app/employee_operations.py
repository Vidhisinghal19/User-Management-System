#app/employee_operations.py

from db import get_connection
import mysql.connector

def get_employee_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT user_id, user_name, email_id, role_id FROM users WHERE user_id = %s", (user_id,))
        employee = cursor.fetchone()
        
        if employee:
            return {
                'user_id': employee['user_id'],
                'user_name': employee['user_name'],
                'email_id': employee['email_id'],
                'role': employee['role_id'],  # Assuming role_id refers to the employee's role
            }
        return {'message': 'Employee not found'}

    except mysql.connector.Error as err:
        return {'message': f'Database error occurred: {str(err)}'}
    except Exception as e:
        return {'message': f'An error occurred: {str(e)}'}
    finally:
        cursor.close()
        connection.close()

def update_employee_profile(user_id, data):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Update the employee's name and email
        cursor.execute(
            "UPDATE users SET user_name = %s, email_id = %s WHERE user_id = %s",
            (data.get('user_name'), data.get('email_id'), user_id)
        )
        connection.commit()  # Commit changes to the database
        
        if cursor.rowcount > 0:
            # Fetch updated profile and return it
            cursor.execute("SELECT user_id, user_name, email_id, role_id FROM users WHERE user_id = %s", (user_id,))
            updated_employee = cursor.fetchone()
            return {
                'message': 'Profile updated successfully',
                'updated_employee': updated_employee
            }
        return {'message': 'Employee not found'}

    except mysql.connector.Error as err:
        return {'message': f'Database error occurred: {str(err)}'}
    except Exception as e:
        return {'message': f'An error occurred: {str(e)}'}
    finally:
        cursor.close()
        connection.close()
