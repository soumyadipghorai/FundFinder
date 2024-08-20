import bcrypt
import os
from dotenv import main

_ = main.load_dotenv(main.find_dotenv())
user_name, password = os.getenv("USER_NAME"), os.getenv("PASSWORD")

users = {
    user_name : bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
}
 
def check_credentials(username, password):
    if username in users:
        return bcrypt.checkpw(password.encode('utf-8'), users[username])
    return False
 
def register_user(username, password):
    if username in users:
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password
    return True