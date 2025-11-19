# Week 8 - Functions for cyber incidents
# CRUD operations for incidents table

import pandas as pd
from app.data.db import connect_database


def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    # Add a new incident to the database
    conn = connect_database()
    cursor = conn.cursor()
    
    # SQL to insert incident
    insert_sql = """
    INSERT INTO cyber_incidents 
    (date, incident_type, severity, status, description, reported_by)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    # Run SQL and save
    cursor.execute(insert_sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    
    # Get the ID of the new incident
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    # Get all incidents from database
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_incident_by_id(incident_id):
    # Get one specific incident
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(incident_id,)
    )
    conn.close()
    return df


def update_incident_status(incident_id, new_status):
    # Change the status of an incident
    conn = connect_database()
    cursor = conn.cursor()
    
    # SQL to update status
    update_sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
    
    # Run SQL and save
    cursor.execute(update_sql, (new_status, incident_id))
    conn.commit()
    
    # Return how many rows changed
    rows_updated = cursor.rowcount
    conn.close()
    return rows_updated


def delete_incident(incident_id):
    # Delete an incident from database
    conn = connect_database()
    cursor = conn.cursor()
    
    # SQL to delete incident
    delete_sql = "DELETE FROM cyber_incidents WHERE id = ?"
    
    # Run SQL and save
    cursor.execute(delete_sql, (incident_id,))
    conn.commit()
    
    # Return how many rows deleted
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted


def get_incidents_by_type_count():
    # Count how many incidents of each type
    conn = connect_database()
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_high_severity_by_status():
    # Count high severity incidents by their status
    conn = connect_database()
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_incident_types_with_many_cases(min_count=5):
    # Find incident types that happen a lot
    conn = connect_database()
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    conn.close()
    return df
