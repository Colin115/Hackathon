import csv
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string

def check_password(username, password, credentials):
    for stored_username, stored_password_hash in credentials:
        if stored_username == username:
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return True
            else:
                return False
    return False  # Return False if username not found

def read_usernames_from_csv(file_path):
    usernames = set()
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                usernames.add(row[0])  # Assuming the username is in the first column
    return usernames

def read_usernames_and_passwords_from_csv(file_path):
    credentials = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Check if the row has both username and password
                credentials[row[0]] = row[1]  # Assuming username is in the first column and password hash in the second
    return credentials

def check_username_exists(username, usernames):
    return username in usernames

def write_usernames_and_passwords_to_csv(file_path, credentials):
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for username, password in credentials:
            hashed_password = hash_password(password)
            writer.writerow([username, hashed_password])

def check_credentials(username, password, credentials):
    if username in credentials:
        hashed_password = credentials[username]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    return False

def check_username_and_password(username, password, file_path):
    credentials = read_usernames_and_passwords_from_csv(file_path)
    return check_credentials(username, password, credentials)

def main():

    
    file_path = 'data.csv'  # Update with the correct input file path
    
    usernames = read_usernames_from_csv(file_path)
    username = input()
    password = input()
    



if __name__ == "__main__":
    main()



