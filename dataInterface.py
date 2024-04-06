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
        if bcrypt.checkpw(password.encode('uft-8'), hashed_password):
            return True
        else:
            return False
    else:
        return None

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def store_username_and_hashed_password(username, hashed_password):
    # Here you would typically store the username and hashed password in a database
    # For demonstration purposes, let's print them
    print("Username:", username)
    print("Hashed Password:", hashed_password)

def main():
    database_file = 'data.csv'
    conn = connect_to_database(database_file)
    username = input("Enter username: ")
    password = input("Enter password: ")
    check_credentials(conn, username, password)
    username, password = get_username_and_password()
    hashed_password = hash_password(password)
    store_username_and_hashed_password(username, hashed_password)
    conn.close()

if __name__ == "__main__":
    main()


