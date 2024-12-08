import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        # Establishing the connection
        connection = mysql.connector.connect(
            host='localhost',
            database='expense_tracking',
            user='root',  # Replace with your MySQL username
            password=''  # Replace with your MySQL password
        )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            
            # Create tables if they don't exist
            cursor = connection.cursor()

            # Create 'users' table if it doesn't exist
            create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
            """
            cursor.execute(create_users_table)

            # Create 'expenses' table if it doesn't exist
            create_expenses_table = """
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10, 2) NOT NULL,
                category VARCHAR(255),
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
            cursor.execute(create_expenses_table)
            connection.commit()
            print("Tables 'users' and 'expenses' are ready.")
        
        return connection

    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Connection closed.")

# Function to register a new user
def register_user(connection, email, password):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, password))
        connection.commit()
        print(f"User {email} registered successfully.")
    except Error as e:
        print(f"Error while registering user: {e}")

# Function to authenticate a user (login)
def authenticate_user(connection, email, password):
    cursor = connection.cursor()
    try:
        query = "SELECT id, email FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        if user:
            print(f"Login successful for {user[1]}")
            return user[0]  # Return the user ID
        else:
            print("Invalid credentials. Please try again.")
            return None
    except Error as e:
        print(f"Error during authentication: {e}")
        return None

