#app/models.py

from db import get_connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Create roles table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
          role_id INT AUTO_INCREMENT PRIMARY KEY,
          role_name VARCHAR(50) NOT NULL UNIQUE
        )
        ''')

        # Create departments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
          department_id INT AUTO_INCREMENT PRIMARY KEY,
          department_name VARCHAR(100) NOT NULL UNIQUE
        )
        ''')

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
          user_id INT AUTO_INCREMENT PRIMARY KEY,
          user_name VARCHAR(50) NOT NULL,
          role_id INT NOT NULL,
          department_id INT,
          email_id VARCHAR(100) NOT NULL UNIQUE,
          passcode VARCHAR(50) NOT NULL,
          FOREIGN KEY (role_id) REFERENCES roles(role_id),
          FOREIGN KEY (department_id) REFERENCES departments(department_id)
        )
        ''')

        connection.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        connection.close()


def insert_initial_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Insert roles if not already present
        cursor.execute("INSERT IGNORE INTO roles (role_name) VALUES ('administrator'), ('manager'), ('employee')")

        # Insert departments if not already present
        cursor.execute("INSERT IGNORE INTO departments (department_name) VALUES ('HR'), ('Marketing'), ('Sales')")

        # Insert users if not already present
        cursor.execute("""
            INSERT IGNORE INTO users (user_name, role_id, department_id, email_id, passcode) 
            VALUES ('vidhi', 1, NULL, 'vidhisinghal5622@gmail.com', 'admin123')
        """)
        

        connection.commit()
    except Exception as e:
        print(f"Error inserting initial data: {e}")
    finally:
        cursor.close()
        connection.close()
