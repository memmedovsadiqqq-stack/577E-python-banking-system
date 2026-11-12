import json
import os
import hashlib
import time

USERS_FILE = "users.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()




def create_default_users():
    data = [
        ("user01", "Test@123", "10010001", 2500.0),
        ("user02", "Test@456", "10010002", 1500.0),
        ("user03", "Test@789", "10010003", 3000.0),
    ]
    users = {}
    for username, password, number, balance in data:
        users[username] = {
            "password_hash": hash_password(password),
            "account_number": number,
            "balance": balance,
            "blocked": False,
            "failed_attempts": 0,
            "lockout_until": 0.0,
            "transactions": []
        }
    return users


def load_users():
    if not os.path.exists(USERS_FILE):
        users = create_default_users()
        save_users(users)
        return users
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Data file is damaged.")
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def countdown(until):
    while True:
        remaining = int(until - time.time())
        if remaining <= 0:
            break
        print(f"Please wait: 00:{remaining:02d}", end="\r")
        time.sleep(1)
    print("Please wait: 00:00")
    print("You may try again.")


def login(users):
    username = input("Username: ").strip()
    if username not in users:
        print("Invalid username or password.")
        return None

    user = users[username]

    if user["blocked"]:
        print("Your card has been blocked.")
        print("Please contact the bank administrator.")
        return None

    if user["lockout_until"] > time.time():
        print("Too many failed login attempts.")
        countdown(user["lockout_until"])

    while True:
        password = input("Password: ")
        if hash_password(password) == user["password_hash"]:
            user["failed_attempts"] = 0
            user["lockout_until"] = 0.0
            save_users(users)
            print(f"Welcome, {username}!")
            return username

        user["failed_attempts"] += 1
        print(f"Incorrect password. Attempt: {user['failed_attempts']}/6")

        if user["failed_attempts"] >= 6:
            user["blocked"] = True
            save_users(users)
            print("Maximum login attempts exceeded.")
            print("Your card has been blocked.")
            print("Please contact the bank administrator.")
            return None

        if user["failed_attempts"] == 3:
            user["lockout_until"] = time.time() + 60
            save_users(users)
            print("Too many failed login attempts.")
            countdown(user["lockout_until"])
        else:
            save_users(users)


def valid_password(password):
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit


def change_password(users, username):
    user = users[username]

    old = input("Current password: ")
    if hash_password(old) != user["password_hash"]:
        print("Current password is incorrect.")
        return

    new = input("New password: ")
    if not valid_password(new):
        print("Password must be at least 8 characters with an uppercase letter, a lowercase letter and a digit.")
        return

    if hash_password(new) == user["password_hash"]:
        print("New password cannot be the same as the old password.")
        return

    again = input("Repeat new password: ")
    if new != again:
        print("Passwords do not match.")
        return

    user["password_hash"] = hash_password(new)
    save_users(users)
    print("Password changed successfully.")


def main():
    users = load_users()
    current_user = login(users)
    if current_user:
        while True:
            print("\n--- MEMBER A MENU ---")
            print("1. Change Password")
            print("2. View Account Info")
            print("3. Logout / Exit")
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                change_password(users, current_user)
            elif choice == "2":
                u = users[current_user]
                print(f"Account Holder: {current_user}")
                print(f"Account Number: {u['account_number']}")
                print(f"Available Balance: {u['balance']:.2f} AZN")
                print(f"Account Status: {'Blocked' if u['blocked'] else 'Active'}")
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()