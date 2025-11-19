# Week 8 - Functions for dataset metadata
# CRUD operations for datasets table

import pandas as pd
from app.data.db import connect_database


def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    # Add a new dataset to database
    conn = connect_database()
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT INTO datasets_metadata 
    (dataset_name, category, source, last_updated, record_count, file_size_mb)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    
    dataset_id = cursor.lastrowid
    conn.close()
    return dataset_id


def get_all_datasets():
    # Get all datasets from database
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def get_dataset_by_id(dataset_id):
    # Get one specific dataset
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata WHERE id = ?",
        conn,
        params=(dataset_id,)
    )
    conn.close()
    return df


def update_dataset_records(dataset_id, new_record_count):
    # Update how many records a dataset has
    conn = connect_database()
    cursor = conn.cursor()
    
    update_sql = "UPDATE datasets_metadata SET record_count = ? WHERE id = ?"
    cursor.execute(update_sql, (new_record_count, dataset_id))
    conn.commit()
    
    rows_updated = cursor.rowcount
    conn.close()
    return rows_updated


def delete_dataset(dataset_id):
    # Remove a dataset from database
    conn = connect_database()
    cursor = conn.cursor()
    
    delete_sql = "DELETE FROM datasets_metadata WHERE id = ?"
    cursor.execute(delete_sql, (dataset_id,))
    conn.commit()
    
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted
