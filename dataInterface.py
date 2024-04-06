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

def read_usernames_passwords_and_social_media_from_csv(file_path):
    credentials = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3:  # Check if the row has username, password, and social media account
                username = row[0]
                hashed_password = row[1]
                social_media = row[2]
                credentials[username] = {'password': hashed_password, 'social_media': social_media}
    return credentials


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
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        username, password, fname, lname, email = credentials
        hashed_password = hash_password(password)
        writer.writerow([username, hashed_password, email, fname, lname, False])

def check_credentials(username, password, credentials):
    if username in credentials:
        hashed_password = credentials[username]['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True
    return False

def check_username_and_password(username, password, file_path):
    credentials = read_usernames_passwords_and_social_media_from_csv(file_path)
    return check_credentials(username, password, credentials)

def read_usernames_passwords_and_social_media_from_csv(file_path):
    credentials = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3:  # Check if the row has username, password, and social media account
                username = row[0]
                hashed_password = row[1]
                social_media = row[2]
                credentials[username] = {'password': hashed_password, 'social_media': social_media}
    return credentials

def read_all_user_select_data_from_csv(file_path, user):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)
            if (row[0] == user):
                username = row[0]
                email = row[2]
                fname = row[3]
                lname = row[4]
                verified = row[5]
                socials = {}
                for col in range(6, len(row)):
                    social = row[col].split(".") # platform.username
                    if socials.get(social[0]):
                        socials[social[0]].append(social[1])
                    else:
                        socials[social[0]] = [social[1]]
                if verified == "True":
                    verified = True
                else:
                    verified = False
                return {'username': username, 'email': email, 'fname': fname, 'lname': lname, 'verified': verified, 'social_media': socials}
            
    return None

def main():

    
    file_path = 'data.csv'  # Update with the correct input file path
    
    usernames = read_usernames_from_csv(file_path)
    username = input()
    password = input()
    



if __name__ == "__main__":
    main()



