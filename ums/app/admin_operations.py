# app/admin_operations.py

from db import get_connection

def create_role(role_name):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO roles (role_name) VALUES (%s)', (role_name,))
        connection.commit()
        print(f"Role '{role_name}' created successfully.")
    except Exception as e:
        print(f"Error creating role: {e}")
    finally:
        cursor.close()
        connection.close()

def create_department(department_name):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO departments (department_name) VALUES (%s)', (department_name,))
        connection.commit()
        print(f"Department '{department_name}' created successfully.")
    except Exception as e:
        print(f"Error creating department: {e}")
    finally:
        cursor.close()
        connection.close()

def create_user(user_name, role_id, department_id, email_id, passcode):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """
            INSERT INTO users (user_name, role_id, department_id, email_id, passcode) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (user_name, role_id, department_id, email_id, passcode)
        cursor.execute(sql, values)
        connection.commit()
        print(f"User '{user_name}' created successfully.")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        cursor.close()
        connection.close()

def read_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error reading users: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_user(user_id, **fields):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        updates = ', '.join(f"{field} = %s" for field in fields.keys())
        values = list(fields.values()) + [user_id]
        query = f"UPDATE users SET {updates} WHERE user_id = %s"
        cursor.execute(query, values)
        connection.commit()
        print(f"User with ID '{user_id}' has been updated.")
    except Exception as e:
        print(f"Error updating user: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        connection.commit()
        print(f"User '{user_id}' deleted.")
    except Exception as e:
        print(f"Error deleting user: {e}")
    finally:
        cursor.close()
        connection.close()
