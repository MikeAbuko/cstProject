# Week 8 - Functions to work with users in the database
# CRUD means Create Read Update Delete

from app.data.db import connect_database


def get_user_by_username(username):
    # Find a user by their username
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def insert_user(username, password_hash, role='user'):
    # Add a new user to the database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_all_users():
    # Get all users from database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def update_user_role(username, new_role):
    # Change a user's role
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (new_role, username)
    )
    conn.commit()
    rows_updated = cursor.rowcount
    conn.close()
    return rows_updated


def delete_user(username):
    # Remove a user from database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM users WHERE username = ?",
        (username,)
    )
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted
