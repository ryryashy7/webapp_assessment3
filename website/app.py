import hashlib
import os
import csv

accounts = []

def accounts_load():
    try:
        with open("website/accounts.csv", "r") as ac:
            for line in ac:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    accounts.append({
                        "username": parts[0],
                        "salt": parts[1],
                        "password_hash": parts[2]
                    })
    except FileNotFoundError:
        print("No accounts file found. Starting with an empty account list.")
accounts_load()

def register():    
    username = input("Username: ")
    password = input("Password: ")

    # Generate random salt
    salt = os.urandom(16)

    # Hash password using scrypt
    password_bytes = password.encode()
    stored_hash = hashlib.scrypt(
        password_bytes,
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    print("=== ACCOUNT CREATED ===\n")

    print("What would be stored in the database:")
    print(f"Username: {username}")
    print(f"Salt: {salt.hex()}")
    print(f"Hash: {stored_hash.hex()}")

    print("\nCombined record:")
    print({
        "username": username,
        "salt": salt.hex(),
        "password_hash": stored_hash.hex()
    })
    register()

# ------------------------
# Login attempt
# ------------------------
def login():
    print("=== LOGIN ===\n")

    entered_username = input("Enter username: ")
    entered_password = input("Enter password: ").encode()

    print("\nUser entered:")
    print(f"Username: {entered_username}")
    print(f"Password: {'*' * len(entered_password)}")

    if entered_username != accounts[0]["username"]:
        print("\nInvalid username")

    else:

        # Hash entered password using the SAME salt
        entered_hash = hashlib.scrypt(
            entered_password,
            salt=accounts[0]["salt"].encode(),
            n=16384,
            r=8,
            p=1
        )

        print("\n=== VERIFICATION PROCESS ===")
        print(f"Stored Salt:   {accounts[0]['salt']}")
        with open("website/accounts.csv", "a") as ac:
            ac.write("{},{},{}\n".format(username, salt.hex(), stored_hash.hex())) #ai help
            
        print(f"Stored Hash:   {accounts[0]['password_hash']}") 
        print(f"Entered Hash:  {entered_hash.hex()}")

        if entered_hash == stored_hash:
            print("\nPassword correct!")
            print("Access granted.")

        else:
            print("\nPassword incorrect!")
            print("Access denied.")
    login()


login_register = input("Do you want to login or register? (L/R) ")
if login_register.lower() == "r":
    register()
elif login_register.lower() == "l":
    login()
else:
    print("Invalid option. Please choose 'L' for login or 'R' for register.")