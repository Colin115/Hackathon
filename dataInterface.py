import sqlite3
import bcrypt

def connect_to_database(database_file):
    conn = sqlite3.connect(database_file)
    return conn

def check_credentials(conn, username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row:
        hashed_password = row[0]
        #check if password matches hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
        else:
            return None
    else:
        return None  # Return False if username not found

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def get_username_and_password():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password

def main():
    database_file = 'your_database.db'  # Update with the correct database file path
    conn = connect_to_database(database_file)
    username, password = get_username_and_password()
    if check_credentials(conn, username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")
    conn.close()

if __name__ == "__main__":
    main()



