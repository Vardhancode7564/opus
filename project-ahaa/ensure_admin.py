import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from database.db import create_user, get_user_by_email, init_db

def ensure_admin():
    init_db()
    email = "adminaah@gmail.com"
    password = "Ahaa@2026"
    user = get_user_by_email(email)
    
    if not user:
        print(f"Creating admin user: {email}")
        if create_user("Admin AHAA", email, password, "admin"):
            print("Admin user created successfully.")
        else:
            print("Failed to create admin user.")
    else:
        print(f"Admin user already exists with role: {user.get('role', 'unknown')}")

if __name__ == "__main__":
    ensure_admin()
