# Week 11 - Authentication Manager Class
# This class handles user authentication in an OOP way

from app.services.user_service import (
    hash_password,
    verify_password,
    validate_username,
    validate_password,
    register_user as register_user_function
)
from app.services.database_manager import DatabaseManager


class AuthManager:
    """
    A class to manage user authentication
    Handles login, registration, and validation
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Constructor - set up auth manager
        
        Parameters:
            db_manager (DatabaseManager) - database manager instance
        """
        self.__db_manager = db_manager
    
    def validate_username(self, username):
        """
        Check if username is valid
        
        Parameters:
            username (str) - username to check
            
        Returns:
            tuple - (is_valid: bool, error_message: str)
        """
        return validate_username(username)
    
    def validate_password(self, password):
        """
        Check if password is valid
        
        Parameters:
            password (str) - password to check
            
        Returns:
            tuple - (is_valid: bool, error_message: str)
        """
        return validate_password(password)
    
    def login(self, username, password):
        """
        Try to login a user
        
        Parameters:
            username (str) - username
            password (str) - plain text password
            
        Returns:
            tuple - (success: bool, user_object or None, error_message: str)
        """
        # Get user object from database
        user = self.__db_manager.get_user_by_username(username)
        
        if not user:
            return False, None, "Username not found"
        
        # Verify password using the User object method
        if verify_password(password, user.get_password_hash()):
            return True, user, "Login successful"
        else:
            return False, None, "Invalid password"
    
    def register(self, username, password, role='user'):
        """
        Register a new user
        
        Parameters:
            username (str) - username
            password (str) - plain text password
            role (str) - user role (default 'user')
            
        Returns:
            tuple - (success: bool, error_message: str)
        """
        # Validate username
        valid_user, user_msg = self.validate_username(username)
        if not valid_user:
            return False, user_msg
        
        # Validate password
        valid_pass, pass_msg = self.validate_password(password)
        if not valid_pass:
            return False, pass_msg
        
        # Check if user already exists
        existing_user = self.__db_manager.get_user_by_username(username)
        if existing_user:
            return False, f"Username '{username}' already exists"
        
        # Register using existing function
        success = register_user_function(username, password, role)
        
        if success:
            return True, "Registration successful"
        else:
            return False, "Registration failed"
    
    def __str__(self):
        """
        String representation
        
        Returns:
            str - description of auth manager
        """
        return "AuthManager handling user authentication"
