#app/manager_operations.py

from db import get_connection

# Fetch the department_id based on the manager's email (logged-in manager)
def get_department_id(manager_email):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Get the department_id of the manager based on their email
            cursor.execute("""
                SELECT department_id 
                FROM users 
                WHERE email_id = %s AND role_id = 2  -- Role ID 2 for managers
            """, (manager_email,))
            
            result = cursor.fetchone()
            department_id = result[0] if result else None
            if department_id:
                print(f"Retrieved department ID for {manager_email}: {department_id}")
            else:
                print(f"No department found for {manager_email}")
            return department_id
    except Exception as e:
        print(f"Error fetching department ID: {e}")
        return None
    finally:
        connection.close()

# Get users in the manager's department
def get_users_in_department(department_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch users in the same department as the manager
            cursor.execute("""
                SELECT u.user_id, u.user_name, u.email_id 
                FROM users u 
                WHERE u.department_id = %s
            """, (department_id,))
            
            # Fetch all rows and convert them into a list of dictionaries
            users = cursor.fetchall()
            return [{"user_id": user[0], "user_name": user[1], "email_id": user[2]} for user in users]
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        connection.close()

# Add a user (as a manager adding users in their department)
def add_user(manager_email, user_name, email_id, passcode):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Get the manager's department ID
            manager_department_id = get_department_id(manager_email)
            
            if manager_department_id is None:
                print("Manager's department not found.")
                return False
            
            # Proceed to add the user in the manager's department
            cursor.execute("""
                INSERT INTO users (user_name, role_id, department_id, email_id, passcode) 
                VALUES (%s, 3, %s, %s, %s)  -- Role ID 3 for regular employees
            """, (user_name, manager_department_id, email_id, passcode))
            connection.commit()
            print(f"User {user_name} added successfully.")
            return True  # Return success flag
    except Exception as e:
        print(f"Error adding user: {e}")
        return False  # Return failure flag
    finally:
        connection.close()

# Update a user's information without COALESCE
def update_user(user_id, user_name, email_id, passcode, manager_department_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the user exists
            cursor.execute("SELECT department_id FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user is None:
                print(f"User {user_id} does not exist.")
                return False
            
            user_department_id = user[0]
            
            # Check if the manager's department matches the user's department
            if user_department_id != manager_department_id:
                print(f"Manager cannot update the user from a different department: User Department ID: {user_department_id}, Manager Department ID: {manager_department_id}")
                return False

            # Proceed to update the user if department check passes
            cursor.execute("""
                UPDATE users 
                SET user_name = %s, email_id = %s, passcode = %s 
                WHERE user_id = %s
            """, (user_name, email_id, passcode, user_id))
            connection.commit()
            print(f"User {user_id} updated successfully.")
            return True
    except Exception as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        connection.close()

# Delete a user
def delete_user(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user is None:
                print(f"User with ID {user_id} does not exist.")
                return False

            print(f"Attempting to delete user with ID: {user_id}")
            # Attempt to delete the user
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            
            # Check if the row was actually deleted
            if cursor.rowcount < 1:  # Adjusted rowcount check
                print(f"Failed to delete user {user_id}.")
                return False

            # Commit the transaction
            connection.commit()
            print(f"User {user_id} deleted successfully.")
            return True

    except Exception as e:
        print(f"Error deleting user: {str(e)}")
        return False

    finally:
        connection.close()
