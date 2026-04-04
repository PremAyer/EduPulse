import psycopg2
import hashlib
from dotenv import load_dotenv
import os

load_dotenv("config/.env")


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_connection():
    # This connects to the database over the internet
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        port=DB_PORT,
        sslmode='require'
        
    )

def create_usertable():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS userstable(
            username TEXT PRIMARY KEY, 
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (%s,%s)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username = %s AND password = %s', (username, password))
    data = c.fetchone()
    conn.close()
    return data

# def update_password(username, new_password):
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('UPDATE userstable SET password = %s WHERE username = %s', (new_password, username))
#     conn.commit()
#     conn.close()

def update_password(email, new_password):
    """Updates the password using raw SQL and returns True on success."""
    try:
        conn = get_connection()
        c = conn.cursor()
        
        # Note: Changed 'username' to 'email' to match your login logic!
        # Make sure your table is actually called 'userstable'
        c.execute('UPDATE userstable SET password = %s WHERE username = %s', (new_password, email))
        
        conn.commit()
        conn.close()
        
        return True # Tells Streamlit it worked!
        
    except Exception as e:
        print(f"Database Error updating password: {e}")
        return False # Tells Streamlit it failed!