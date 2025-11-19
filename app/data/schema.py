# Week 8 - Creating all the database tables
# This file has all the SQL code to make tables

def create_users_table(conn):
    # Make the users table
    cursor = conn.cursor()
    
    # SQL code for users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ Users table created successfully!")


def create_cyber_incidents_table(conn):
    # Make table for cyber incidents
    cursor = conn.cursor()
    
    # SQL code for cyber_incidents table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Run the SQL
    cursor.execute(create_table_sql)
    
    # Save to database
    conn.commit()
    
    # Print message
    print("✅ Cyber incidents table created successfully!")


def create_datasets_metadata_table(conn):
    # Make table for dataset info
    cursor = conn.cursor()
    
    # SQL code for datasets table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Run SQL
    cursor.execute(create_table_sql)
    conn.commit()
    
    # Print message
    print("✅ Datasets metadata table created successfully!")


def create_it_tickets_table(conn):
    # Make table for IT tickets
    cursor = conn.cursor()
    
    # SQL code for tickets table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Run SQL
    cursor.execute(create_table_sql)
    conn.commit()
    
    # Print message
    print("✅ IT tickets table created successfully!")


def create_all_tables(conn):
    # Call all functions to make all tables
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("\n✅ All tables created successfully!")
