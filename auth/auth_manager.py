"""
Authentication Manager - Smart Records System

This module handles all user authentication operations including:
- User registration (creating new accounts)
- User login (verifying username and password)
- Password hashing (storing passwords securely)
- Session management (tracking who is currently logged in)

SECURITY NOTE: Passwords are hashed using SHA-256 before storing in the database.
This means the actual password is never stored - only a hash (encrypted version).
"""

# Import hashlib - Python's built-in library for hashing (encrypting) data
# We use this to hash passwords so they're not stored in plain text
import hashlib


class AuthManager:
    """
    Authentication Manager Class
    
    This class manages user authentication for the Smart Records System.
    It handles login, registration, and password security.
    
    Think of this as a "security guard" that checks IDs and manages access.
    """
    
    def __init__(self, db_manager):
        """
        Initialize the authentication manager.
        
        Args:
            db_manager: DatabaseManager instance - used to access the database
                       to check usernames, passwords, and create new users
        """
        # Store reference to database manager so we can query the database
        # This is like having a connection to the user database
        self.db = db_manager
        
        # Track the currently logged-in user
        # None means no one is logged in
        # When user logs in, this will contain {'id': user_id, 'username': username}
        self.current_user = None
    
    @staticmethod
    def hash_password(password):
        """
        Hash (encrypt) a password using SHA-256 algorithm.
        
        This is a static method (doesn't need an instance of the class to call).
        We hash passwords so they're never stored in plain text - much more secure!
        
        Args:
            password (str): The plain text password to hash
            
        Returns:
            str: The hashed password (a long string of characters)
            
        Example:
            hash_password("mypassword123") returns something like:
            "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94"
        """
        # Convert password string to bytes (required for hashing)
        # .encode() converts text to bytes using UTF-8 encoding
        password_bytes = password.encode()
        
        # Create SHA-256 hash object
        # SHA-256 is a secure hashing algorithm that converts data into a fixed-size string
        hash_object = hashlib.sha256(password_bytes)
        
        # Get the hexadecimal representation of the hash
        # hexdigest() returns the hash as a string of hexadecimal characters
        hashed_password = hash_object.hexdigest()
        
        # Return the hashed password
        return hashed_password
    
    def register_user(self, username, password):
        """
        Register a new user account.
        
        This method creates a new user account after validating the input.
        It checks if username is available and password meets requirements.
        
        Args:
            username (str): The desired username (must be unique)
            password (str): The desired password (must be at least 8 characters)
            
        Returns:
            tuple: (success: bool, message: str)
                   - success: True if registration succeeded, False otherwise
                   - message: Human-readable message explaining the result
        """
        # Validate username - check if it's not empty
        # .strip() removes leading/trailing whitespace
        # not username.strip() is True if username is empty or only spaces
        if not username or not username.strip():
            # Return failure with error message
            return False, "Username is required"
        
        # Validate password - must be at least 8 characters long
        # This is a basic security requirement
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Check if username already exists in database
        # execute_query() runs a SQL SELECT query and returns results
        # %s is a placeholder that gets replaced with username.strip() (prevents SQL injection)
        existing = self.db.execute_query("SELECT id FROM users WHERE username = %s", (username.strip(),))
        
        # If any results were returned, username already exists
        if existing:
            return False, "Username already exists"
        
        # Hash the password before storing it
        # Never store plain text passwords!
        hashed_password = self.hash_password(password)
        
        # Try to insert the new user into the database
        try:
            # execute_update() runs INSERT, UPDATE, or DELETE queries
            # INSERT INTO creates a new row in the users table
            # VALUES (%s, %s) inserts the username and hashed password
            self.db.execute_update(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username.strip(), hashed_password)  # Parameters to replace %s placeholders
            )
            # Registration successful!
            return True, "User registered successfully"
        except Exception as e:
            # If something goes wrong (database error, etc.), return error message
            # str(e) converts the exception to a readable string
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username, password):
        """
        Authenticate a user (log them in).
        
        This method checks if the username and password are correct.
        If correct, it sets the current_user to track who is logged in.
        
        Args:
            username (str): The username to check
            password (str): The password to verify
            
        Returns:
            tuple: (success: bool, message: str)
                   - success: True if login succeeded, False otherwise
                   - message: Human-readable message explaining the result
        """
        # Validate that both username and password were provided
        if not username or not password:
            return False, "Username and password are required"
        
        # Query database to find user with matching username
        # SELECT * gets all columns from the users table
        # WHERE username = %s filters to only matching username
        users = self.db.execute_query("SELECT * FROM users WHERE username = %s", (username.strip(),))
        
        # Check if user was found
        # If list is empty, username doesn't exist
        if not users:
            # Don't say "username doesn't exist" - that's a security risk
            # Instead say "invalid username or password" so attackers can't enumerate usernames
            return False, "Invalid username or password"
        
        # Get the first (and should be only) user from results
        # users[0] gets the first item in the list
        user = users[0]
        
        # Hash the provided password using the same algorithm
        # We need to compare the hashed version with what's stored in database
        hashed_password = self.hash_password(password)
        
        # Compare the hashed password with the stored password hash
        # If they match, password is correct
        if user['password'] != hashed_password:
            return False, "Invalid username or password"
        
        # Login successful! Store the current user information
        # This tracks who is logged in for the current session
        self.current_user = {
            'id': user['id'],           # User's unique ID from database
            'username': user['username'] # User's username
        }
        
        return True, "Login successful"
    
    def logout(self):
        """
        Log out the current user.
        
        This clears the current_user, effectively ending the user's session.
        After logout, user must login again to access the system.
        """
        # Set current_user to None - no one is logged in anymore
        self.current_user = None
    
    def is_authenticated(self):
        """
        Check if a user is currently logged in.
        
        Returns:
            bool: True if user is logged in, False otherwise
        """
        # Return True if current_user is not None (someone is logged in)
        # Return False if current_user is None (no one is logged in)
        return self.current_user is not None
    
    def get_current_user(self):
        """
        Get information about the currently logged-in user.
        
        Returns:
            dict or None: Dictionary with user info if logged in, None otherwise
                         Format: {'id': user_id, 'username': username}
        """
        # Return the current_user dictionary (or None if not logged in)
        return self.current_user
