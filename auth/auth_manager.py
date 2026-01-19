"""Authentication and user management."""

import hashlib


class AuthManager:
    """Manages user authentication and registration."""
    
    def __init__(self, db_manager):
        """Initialize authentication manager."""
        self.db = db_manager
        self.current_user = None
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        """Register new user. Returns (success, message) tuple."""
        if not username or not username.strip():
            return False, "Username is required"
        
        if not password or len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        existing = self.db.execute_query("SELECT id FROM users WHERE username = %s", (username.strip(),))
        if existing:
            return False, "Username already exists"
        
        hashed_password = self.hash_password(password)
        try:
            self.db.execute_update(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username.strip(), hashed_password)
            )
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def login(self, username, password):
        """Authenticate user. Returns (success, message) tuple."""
        if not username or not password:
            return False, "Username and password are required"
        
        users = self.db.execute_query("SELECT * FROM users WHERE username = %s", (username.strip(),))
        if not users:
            return False, "Invalid username or password"
        
        user = users[0]
        hashed_password = self.hash_password(password)
        if user['password'] != hashed_password:
            return False, "Invalid username or password"
        
        self.current_user = {'id': user['id'], 'username': user['username']}
        return True, "Login successful"
    
    def logout(self):
        """Log out current user."""
        self.current_user = None
    
    def is_authenticated(self):
        """Check if user is authenticated."""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current authenticated user. Returns user dict or None."""
        return self.current_user

