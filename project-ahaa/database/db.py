import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

def init_db():
    """Initializes the SQLite user database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'admin'))
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hashes a plain-text password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plain-text password against a hashed one."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(name, email, password, role):
    """Creates a new user in the database."""
    hashed = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Retrieves a user record by email."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    init_db()
    # Create demo users if they don't exist
    if not get_user_by_email("student@test.com"):
        create_user("Student User", "student@test.com", "student123", "student")
        print("Created demo student: student@test.com / student123")
    if not get_user_by_email("admin@test.com"):
        create_user("Admin User", "admin@test.com", "admin123", "admin")
        print("Created demo admin: admin@test.com / admin123")
