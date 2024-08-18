import bcrypt

# In-memory user storage for simplicity
users = {
    "admin": bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
}

# Function to check credentials
def check_credentials(username, password):
    if username in users:
        return bcrypt.checkpw(password.encode('utf-8'), users[username])
    return False

# Function to register a new user
def register_user(username, password):
    if username in users:
        return False  # User already exists
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password
    return True