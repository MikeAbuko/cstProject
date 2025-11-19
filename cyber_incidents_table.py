import sqlite3

conn = sqlite3.connect('Data/it_tickets.csv')
dbObject = conn.cursor()

createScript = """create table if not exists it_tickets(
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
    created_at )"""
 
dbObject.execute(createScript)
conn.commit()
print("Users table created successfully!")