# Week 11 - Database Manager Class
# This class handles all database operations in an OOP way

import sqlite3
from pathlib import Path
from typing import List, Optional
from models.user import User
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket


class DatabaseManager:
    """
    A class to manage database operations
    Wraps all database connections and queries
    """
    
    def __init__(self, db_path="DATA/intelligence_platform.db"):
        """
        Constructor - set up database connection
        
        Parameters:
            db_path (str) - path to SQLite database file
        """
        self.__db_path = Path(db_path)
        self.__connection = None
    
    def connect(self):
        """Open connection to database"""
        if self.__connection is None:
            self.__connection = sqlite3.connect(str(self.__db_path))
    
    def close(self):
        """Close database connection"""
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None
    
    def execute_query(self, sql, params=()):
        """
        Execute a write query (INSERT, UPDATE, DELETE)
        
        Parameters:
            sql (str) - SQL query to execute
            params (tuple) - parameters for query
            
        Returns:
            cursor - database cursor
        """
        if self.__connection is None:
            self.connect()
        
        cursor = self.__connection.cursor()
        cursor.execute(sql, params)
        self.__connection.commit()
        return cursor
    
    def fetch_one(self, sql, params=()):
        """
        Fetch one row from database
        
        Parameters:
            sql (str) - SQL query
            params (tuple) - parameters for query
            
        Returns:
            tuple - one row of data, or None
        """
        if self.__connection is None:
            self.connect()
        
        cursor = self.__connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchone()
    
    def fetch_all(self, sql, params=()):
        """
        Fetch all rows from database
        
        Parameters:
            sql (str) - SQL query
            params (tuple) - parameters for query
            
        Returns:
            list - list of tuples (rows)
        """
        if self.__connection is None:
            self.connect()
        
        cursor = self.__connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    
    # USER OPERATIONS
    
    def get_user_by_username(self, username):
        """
        Get a user by username, returns User object
        
        Parameters:
            username (str) - username to search for
            
        Returns:
            User object or None
        """
        sql = "SELECT username, password_hash, role FROM users WHERE username = ?"
        row = self.fetch_one(sql, (username,))
        
        if row:
            return User(username=row[0], password_hash=row[1], role=row[2])
        return None
    
    # INCIDENT OPERATIONS
    
    def get_all_incidents(self) -> List[SecurityIncident]:
        """
        Get all security incidents as objects
        
        Returns:
            list - list of SecurityIncident objects
        """
        sql = "SELECT id, date, incident_type, severity, status, description, reported_by FROM cyber_incidents ORDER BY id DESC"
        rows = self.fetch_all(sql)
        
        incidents = []
        for row in rows:
            incident = SecurityIncident(
                incident_id=row[0],
                date=row[1],
                incident_type=row[2],
                severity=row[3],
                status=row[4],
                description=row[5],
                reported_by=row[6]
            )
            incidents.append(incident)
        
        return incidents
    
    def get_incident_by_id(self, incident_id) -> Optional[SecurityIncident]:
        """
        Get one incident by ID
        
        Parameters:
            incident_id (int) - incident ID to find
            
        Returns:
            SecurityIncident object or None
        """
        sql = "SELECT id, date, incident_type, severity, status, description, reported_by FROM cyber_incidents WHERE id = ?"
        row = self.fetch_one(sql, (incident_id,))
        
        if row:
            return SecurityIncident(
                incident_id=row[0],
                date=row[1],
                incident_type=row[2],
                severity=row[3],
                status=row[4],
                description=row[5],
                reported_by=row[6]
            )
        return None
    
    def insert_incident(self, incident: SecurityIncident) -> int:
        """
        Insert a new incident into database
        
        Parameters:
            incident (SecurityIncident) - incident object to insert
            
        Returns:
            int - ID of newly created incident
        """
        sql = """
        INSERT INTO cyber_incidents 
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(sql, (
            incident.get_date(),
            incident.get_incident_type(),
            incident.get_severity(),
            incident.get_status(),
            incident.get_description(),
            incident.get_reported_by()
        ))
        return cursor.lastrowid
    
    def update_incident_status(self, incident_id, new_status):
        """
        Update an incident's status
        
        Parameters:
            incident_id (int) - incident ID
            new_status (str) - new status value
            
        Returns:
            int - number of rows updated
        """
        sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"
        cursor = self.execute_query(sql, (new_status, incident_id))
        return cursor.rowcount
    
    def delete_incident(self, incident_id):
        """
        Delete an incident
        
        Parameters:
            incident_id (int) - incident ID to delete
            
        Returns:
            int - number of rows deleted
        """
        sql = "DELETE FROM cyber_incidents WHERE id = ?"
        cursor = self.execute_query(sql, (incident_id,))
        return cursor.rowcount
    
    # DATASET OPERATIONS
    
    def get_all_datasets(self) -> List[Dataset]:
        """
        Get all datasets as objects
        
        Returns:
            list - list of Dataset objects
        """
        sql = "SELECT id, dataset_name, file_size_mb, record_count, source, category FROM datasets_metadata ORDER BY id DESC"
        rows = self.fetch_all(sql)
        
        datasets = []
        for row in rows:
            # Convert MB to bytes for Dataset class
            size_bytes = int(row[2] * 1024 * 1024) if row[2] else 0
            dataset = Dataset(
                dataset_id=row[0],
                name=row[1],
                size_bytes=size_bytes,
                rows=row[3],
                source=row[4],
                format_type=row[5]
            )
            datasets.append(dataset)
        
        return datasets
    
    def insert_dataset(self, dataset_name, category, source, last_updated, record_count, file_size_mb):
        """
        Insert a new dataset into database
        
        Parameters:
            dataset_name (str) - name of dataset
            category (str) - dataset category
            source (str) - where dataset came from
            last_updated (str) - when it was updated
            record_count (int) - number of records
            file_size_mb (float) - size in megabytes
            
        Returns:
            int - ID of newly created dataset
        """
        sql = """
        INSERT INTO datasets_metadata 
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(sql, (
            dataset_name, category, source, last_updated, record_count, file_size_mb
        ))
        return cursor.lastrowid
    
    # TICKET OPERATIONS 
    
    def get_all_tickets(self) -> List[ITTicket]:
        """
        Get all IT tickets as objects
        
        Returns:
            list - list of ITTicket objects
        """
        sql = "SELECT id, ticket_id, subject, priority, status, category, assigned_to, created_date FROM it_tickets ORDER BY id DESC"
        rows = self.fetch_all(sql)
        
        tickets = []
        for row in rows:
            ticket = ITTicket(
                ticket_id=row[0],  # database id
                title=row[2],  # subject
                priority=row[3],
                status=row[4],
                category=row[5],
                assigned_to=row[6],
                created_date=row[7]
            )
            tickets.append(ticket)
        
        return tickets
    
    def get_ticket_by_id(self, ticket_id) -> Optional[ITTicket]:
        """
        Get one ticket by ID
        
        Parameters:
            ticket_id (int) - ticket ID
            
        Returns:
            ITTicket object or None
        """
        sql = "SELECT id, ticket_id, subject, priority, status, category, assigned_to, created_date FROM it_tickets WHERE id = ?"
        row = self.fetch_one(sql, (ticket_id,))
        
        if row:
            return ITTicket(
                ticket_id=row[0],
                title=row[2],
                priority=row[3],
                status=row[4],
                category=row[5],
                assigned_to=row[6],
                created_date=row[7]
            )
        return None
    
    def insert_ticket(self, ticket_id, priority, status, category, subject, description, created_date, resolved_date=None, assigned_to=None):
        """
        Insert a new ticket
        
        Parameters:
            ticket_id (str) - ticket ID
            priority (str) - priority
            status (str) - status
            category (str) - category
            subject (str) - subject
            description (str) - description
            created_date (str) - date created
            resolved_date (str) - date resolved (optional)
            assigned_to (str) - assigned to (optional)
            
        Returns:
            int - new ticket database ID
        """
        sql = """
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(sql, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
        return cursor.lastrowid
    
    def update_ticket_status(self, ticket_id, new_status):
        """
        Update ticket status
        
        Parameters:
            ticket_id (int) - ticket database ID
            new_status (str) - new status
            
        Returns:
            int - rows updated
        """
        sql = "UPDATE it_tickets SET status = ? WHERE id = ?"
        cursor = self.execute_query(sql, (new_status, ticket_id))
        return cursor.rowcount
    
    def delete_ticket(self, ticket_id):
        """
        Delete a ticket
        
        Parameters:
            ticket_id (int) - ticket database ID
            
        Returns:
            int - rows deleted
        """
        sql = "DELETE FROM it_tickets WHERE id = ?"
        cursor = self.execute_query(sql, (ticket_id,))
        return cursor.rowcount
