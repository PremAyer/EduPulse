# import sqlite3
# import hashlib


import psycopg2
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Replace these with the details from your Supabase Dashboard
#DB_URI = "postgresql://postgres:Supabase%40145230@db.rkrqmqfewuugesgodxms.supabase.co:5432/postgres"
DB_HOST="aws-1-ap-northeast-2.pooler.supabase.com"
DB_USER="postgres.rkrqmqfewuugesgodxms"
DB_PASS="Supabase@145230"
DB_NAME="postgres"
DB_PORT="6543"


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

def update_password(username, new_password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE userstable SET password = %s WHERE username = %s', (new_password, username))
    conn.commit()
    conn.close()


# # Function to encrypt passwords
# def make_hashes(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()

# def check_hashes(password, hashed_text):
#     if make_hashes(password) == hashed_text:
#         return hashed_text
#     return False

# # Database functions
# def create_usertable():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
#     conn.commit()
#     conn.close()

# def add_userdata(username, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
#     conn.commit()
#     conn.close()

# def login_user(username, password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
#     data = c.fetchall()
#     conn.close()
#     return data

# def update_password(username, new_password):
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('UPDATE userstable SET password = ? WHERE username = ?', (new_password, username))
#     conn.commit()
#     conn.close()


