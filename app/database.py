import sqlite3 
import os 

def init_db():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('instance/notes.db')
    conn.row_factory = sqlite3.Row
    return conn


# first hole : SQL injection

def authenticate_user(username, password):
    #direct string concatentation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query) # no parameterization
    user = cursor.fetchone()
    conn.close()

    return user

# no protection against SQL injection 
 
def register_user(username, password):
    #direct string concatenation 
    query 