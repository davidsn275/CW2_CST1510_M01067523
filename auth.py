import bcrypt 
import os

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    # Encode the stored hash to bytes (if it's a string)
    if isinstance(hashed_password, str):
        hashed_password_bytes = hashed_password.encode('utf-8')
    else:
        hashed_password_bytes = hashed_password
    # Use bcrypt.checkpw() to verify the password
    # bcrypt.checkpw handles extracting the salt and comparing
    try:
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    except ValueError:
        # If there's an error, the hash is corrupted or invalid
        return False

    
def register_user(username, password):

    # Check if the username already exists
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    # Hash the password
    hashed_password = hash_password(password)

    # Append the new user to the file
    # Format: username,hashed_password
    try:
        with open(USER_DATA_FILE, 'a') as f:
            f.write(f"{username},{hashed_password}\n")
        print(f"Success: User '{username}' registered successfully!")
        return True
    except IOError as e:
        print(f"Error: Could not save user data. {e}")
        return False

def user_exists(username):
    # Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    try:
        # Read the file and check each line for the username
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                stored_username = line.strip().split(',', 1)[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False
    
    return False
 
def login_user(username, password):
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("Error: Username not found.")
        return False
    
    try:
        # Search for the username in the file
        with open(USER_DATA_FILE, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                stored_username, stored_hash = line.split(',', 1)

                # If username matches, verify the password
                if stored_username == username:
                    if verify_password(password, stored_hash):
                        print(f"Success: Welcome, {username}!")
                        return True
                    else:
                        print("Error: Invalid password.")
                        return False
        # If we reach here, the username was not found
        print("Error: Username not found.")
        return False
    except IOError as e:
        print(f"Error: Could not read user data. {e}")
        return False
    
def validate_username(username):
    # Check length (3-20 characters)
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username must be at most 20 characters long."

    # Check if alphanumeric only
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    
    return True, ""

def validate_password(password):
    # Check length (6-50 characters)
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if len(password) > 50:
        return False, "Password must be at most 50 characters long."
    
    return True, ""

def check_password_strength(password):
    score = 0

    # length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1

    # Character diversity checks
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    # ASCII 33-47, 58-64, 91-96, 123-126: Special characters
    if any(ord(c) in range(33, 48) or ord(c) in range(58, 65) or ord(c) in range(91, 97) or ord(c) in range(123, 127) for c in password):
        score += 1

    # Determine strength
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard)")
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


# TEMPORARY TEST CODE - Remove after testing
if __name__ == "__main__":
    main()