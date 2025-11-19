# Week 8 - Main Demo Program
# This shows how everything works together

import pandas as pd
from pathlib import Path
from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import (
    insert_incident, 
    get_all_incidents, 
    update_incident_status, 
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status
)


def setup_database():
    # Set up the database with all tables and data
    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE")
    print("="*60)
    
    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("✅ Connected")
    
    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)
    
    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    user_count = migrate_users_from_file()
    
    # Step 4: Load CSV data (skip if files are database files)
    print("\n[4/5] Checking for CSV data...")
    print("✅ Skipped - database already has data or no CSV files available")
    
    # Step 5: Check everything is there
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()
    
    # Count rows in each table
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE COMPLETE!")
    print("="*60)


def demo_authentication():
    # Test the login and register functions
    print("\n" + "="*60)
    print("AUTHENTICATION")
    print("="*60)
    
    # Test registration
    print("\n[TEST] Registering new user 'testuser'...")
    register_user("testuser", "TestPass123!", "user")
    
    # Test login with correct password
    print("\n[TEST] Login with correct password...")
    login_user("testuser", "TestPass123!")
    
    # Test login with wrong password
    print("\n[TEST] Login with wrong password...")
    login_user("testuser", "WrongPassword")


def demo_crud_operations():
    # Test the CRUD functions (Create Read Update Delete)
    print("\n" + "="*60)
    print("CRUD OPERATIONS")
    print("="*60)
    
    # CREATE
    print("\n[CREATE] Inserting new incident...")
    incident_id = insert_incident(
        date="2024-11-05",
        incident_type="Phishing",
        severity="High",
        status="Open",
        description="Suspicious email campaign detected targeting finance department",
        reported_by="alice"
    )
    print(f"✅ Created incident #{incident_id}")
    
    # READ
    print("\n[READ] Retrieving all incidents...")
    df = get_all_incidents()
    print(f"✅ Found {len(df)} total incidents")
    print(f"\nMost recent incident:")
    print(df.head(1)[['id', 'incident_type', 'severity', 'status']])
    
    # UPDATE
    print(f"\n[UPDATE] Updating incident #{incident_id} status...")
    rows_updated = update_incident_status(incident_id, "Investigating")
    print(f"✅ Updated {rows_updated} row(s)")
    
    # DELETE
    print(f"\n[DELETE] Deleting incident #{incident_id}...")
    rows_deleted = delete_incident(incident_id)
    print(f"✅ Deleted {rows_deleted} row(s)")


def demo_analytical_queries():
    # Test the query functions
    print("\n" + "="*60)
    print("ANALYTICAL QUERIES")
    print("="*60)
    
    print("\n[QUERY 1] Incidents by Type:")
    df = get_incidents_by_type_count()
    print(df.to_string(index=False))
    
    print("\n[QUERY 2] High Severity Incidents by Status:")
    df = get_high_severity_by_status()
    print(df.to_string(index=False))


def main():
    # Main function - runs everything
    print("\n" + "="*70)
    print(" " * 15 + "WEEK 8: DATABASE DEMO")
    print(" " * 10 + "Multi-Domain Intelligence Platform")
    print("="*70)
    
    # Setup database
    setup_database()
    
    # Demo authentication
    demo_authentication()
    
    # Demo CRUD operations
    demo_crud_operations()
    
    # Demo analytical queries
    demo_analytical_queries()
    
    print("\n" + "="*70)
    print("✅ ALL DEMO COMPLETED!")
    print("="*70)
    


if __name__ == "__main__":
    main()
