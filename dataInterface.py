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

def find_username_from_social_account(social_username: str, platform: str, file_path: str):
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row > 6):
                for i in range(6, len(row)):
                    if (row[i].split(".")[1] == social_username):
                        return row[0]
    return None

def add_social_media_account(username, social_username, platform, file_path):
    # Read existing data from the CSV file
    rows = []
    row_index = -1
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if len(row) > 0 and username == row[0]:
                row_index = i
            rows.append(row)

    # Check if the row index is valid
    if row_index == -1:
        return

    # Add data to the end of the specified row
    rows[row_index].append(f'{platform}.{social_username}')

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

def remove_social_media_account(username, social_username, platform, file_path):
        # Read existing data from the CSV file
    rows: list = []
    row_index = -1
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if len(row) > 0 and username == row[0]:
                row_index = i
            rows.append(row)

    # Check if the row index is valid
    if row_index == -1:
        return

    # Add remove specified row based on username
    rows[row_index].remove(f'{platform}.{social_username}')

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

def updated_verified(username, file_path):
            # Read existing data from the CSV file
    rows: list = []
    row_index = -1
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            if len(row) > 0 and username == row[0]:
                row_index = i
            rows.append(row)

    # Check if the row index is valid
    if row_index == -1:
        return

    # Add remove specified row based on username
    if len(rows[row_index]) >= 6:
        rows[row_index][5] = "True"

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

def main():

    
    file_path = 'data.csv'  # Update with the correct input file path
    
    usernames = read_usernames_from_csv(file_path)
    username = input()
    password = input()
    



if __name__ == "__main__":
    main()



