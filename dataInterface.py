import csv

def read_usernames_and_passwords_from_csv(file_path):
    credentials = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Check if the row has both username and password
                credentials.append((row[0], row[1]))  # Assuming username is in the first column and password in the second
    return credentials

def main():
    file_path = 'data.csv'  # Update with the correct file path
    credentials = read_usernames_and_passwords_from_csv(file_path)
    print("Usernames and passwords from CSV:")
    for username, password in credentials:
        print("Username:", username, "Password:", password)

if __name__ == "__main__":
    main()



