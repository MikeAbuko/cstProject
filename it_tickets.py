import sqlite3

conn = sqlite3.connect('Data/cyber_incidents.csv')
dbObject = conn.cursor()

createScript = """create table if not exists cyber_incidents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    incident_type TEXT,
    severity TEXT,
    status TEXT,
    description TEXT,
    reported_by TEXT,
    created_at TEXT)"""
 
dbObject.execute(createScript)
conn.commit()
print("Users table created successfully!")