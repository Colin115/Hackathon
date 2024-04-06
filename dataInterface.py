import csv
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string

def read_usernames_and_passwords_from_csv(file_path):
    credentials = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Check if the row has both username and password
                credentials.append((row[0], row[1]))  # Assuming username is in the first column and password in the second
    return credentials

def write_usernames_and_passwords_to_csv(file_path, credentials):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for username, password in credentials:
            hashed_password = hash_password(password)
            writer.writerow([username, hashed_password])

def main():
    input_file_path = 'data.csv'  # Update with the correct input file path
    output_file_path = 'data.csv'  # Update with the correct output file path
    
    # Read usernames and passwords from plain CSV
    credentials = read_usernames_and_passwords_from_csv(input_file_path)
    
    # Write encrypted usernames and passwords to a new CSV
    write_usernames_and_passwords_to_csv(output_file_path, credentials)
    
    print("Usernames and passwords encrypted and written to:", output_file_path)


if __name__ == "__main__":
    main()



