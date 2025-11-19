import sqlite3

conn = sqlite3.connect('Data/datasets_metadata.csv')
dbObject = conn.cursor()

createScript = """create table if not exists datasets_metadata(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_name TEXT NOT NULL,
    category TEXT,
    source TEXT,
    last_updated TEXT,
    record_count INTEGER,
    file_size_mb REAL,
    created_at TEXT)"""
 
dbObject.execute(createScript)
conn.commit()
print("Users table created successfully!")