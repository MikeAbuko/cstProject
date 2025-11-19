"""
User service functions - Authentication and User Migration.
Week 8 - CST1510
Migrated from Week 7 auth.py to use database instead of text file
"""

import bcrypt
import sqlite3
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user


def hash_password(plain_text_pass):
    """Hash a plaintext password and return the hash as a UTF-8 string."""
    pass_bytes = plain_text_pass.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    return hashed_pass.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    """Verify a plaintext password against a stored hash (str or bytes)."""
    password_bytes = plain_text_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password_bytes = hashed_password.encode('utf-8')
    else:
        hashed_password_bytes = hashed_password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def user_exists(username):
    """Check if user exists in database."""
    user = get_user_by_username(username)
    return user is not None


def register_user(username, password, role='user'):
    """
    Register a new user in the database.
    Migrated from Week 7 auth.py
    """
    if user_exists(username):
        print(f"Error: Username {username} already exists.")
        return False
    
    hashed_password = hash_password(password)
    
    try:
        insert_user(username, hashed_password, role)
        print(f"Success: User '{username}' registered successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def login_user(username, password):
    """
    Authenticate a user against the database.
    Migrated from Week 7 auth.py
    """
    user = get_user_by_username(username)
    
    if not user:
        print("Error: Username not found.")
        return False
    
    # user[2] is password_hash column
    stored_hash = user[2]
    
    if verify_password(password, stored_hash):
        print(f"Success: Welcome, {username}!")
        return True
    else:
        print("Error: Invalid password.")
        return False


def validate_username(username):
    """Return (is_valid: bool, error_message: str)."""
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters."
    if not username.isalnum():
        return False, "Username cannot contain special characters."
    return True, ""


def validate_password(password):
    """Return (is_valid: bool, error_message: str)."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    return True, ""


def migrate_users_from_file(filepath='DATA/users.txt'):
    """
    Migrate users from users.txt to the database.
    
    Args:
        filepath: Path to users.txt file
        
    Returns:
        int: Number of users migrated
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        print("   No users to migrate.")
        return 0
    
    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse line: username,password_hash
            parts = line.split(',', 1)
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]
                role = 'user'
                
                # Insert user (ignore if already exists)
                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, role)
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except sqlite3.Error as e:
                    print(f"Error migrating user {username}: {e}")
    
    conn.commit()
    conn.close()
    print(f"✅ Migrated {migrated_count} users from {filepath.name}")
    return migrated_count
