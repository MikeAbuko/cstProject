# Week 8 - Functions for IT tickets
# CRUD operations for tickets table

import pandas as pd
from app.data.db import connect_database


def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, resolved_date=None, assigned_to=None):
    # Add a new ticket to database
    conn = connect_database()
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO it_tickets 
    (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    conn.commit()
    
    id = cursor.lastrowid
    conn.close()
    return id


def get_all_tickets():
    # Get all tickets from database
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_ticket_by_id(ticket_id):
    # Get one specific ticket
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets WHERE id = ?",
        conn,
        params=(ticket_id,)
    )
    conn.close()
    return df


def update_ticket_status(ticket_id, new_status):
    # Change the status of a ticket
    conn = connect_database()
    cursor = conn.cursor()
    
    update_sql = "UPDATE it_tickets SET status = ? WHERE id = ?"
    cursor.execute(update_sql, (new_status, ticket_id))
    conn.commit()
    
    rows_updated = cursor.rowcount
    conn.close()
    return rows_updated


def delete_ticket(ticket_id):
    # Remove a ticket from database
    conn = connect_database()
    cursor = conn.cursor()
    
    delete_sql = "DELETE FROM it_tickets WHERE id = ?"
    cursor.execute(delete_sql, (ticket_id,))
    conn.commit()
    
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted
