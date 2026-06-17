import hashlib
import os

# ------------------------
# Create user account
# ------------------------

username = input("Create a username: ")
password = input("Create a password: ").encode()

# Generate random salt
salt = os.urandom(16)

# Hash password using scrypt
stored_hash = hashlib.scrypt(
    password,
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

print("\nNotice that the password is NOT stored.\n")

# ------------------------
# Login attempt
# ------------------------

print("=== LOGIN ===\n")

entered_username = input("Enter username: ")
entered_password = input("Enter password: ").encode()

print("\nUser entered:")
print(f"Username: {entered_username}")
print(f"Password: {'*' * len(entered_password)}")

if entered_username != username:
    print("\nInvalid username")

else:

    # Hash entered password using the SAME salt
    entered_hash = hashlib.scrypt(
        entered_password,
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    print("\n=== VERIFICATION PROCESS ===")
    print(f"Stored Salt:   {salt.hex()}")
    print(f"Stored Hash:   {stored_hash.hex()}")
    print(f"Entered Hash:  {entered_hash.hex()}")

    if entered_hash == stored_hash:
        print("\nPassword correct!")
        print("Access granted.")

    else:
        print("\nPassword incorrect!")
        print("Access denied.")