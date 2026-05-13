from database.db_connection import get_db_connection
from psycopg2.extras import DictCursor
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, full_name, email, password_hash, is_verified, profile_image, phone, bio, address, created_at):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.is_verified = is_verified
        self.profile_image = profile_image
        self.phone = phone
        self.bio = bio
        self.address = address
        self.created_at = created_at

def get_user_object(user_row):
    if user_row:
        return User(
            id=user_row['id'],
            full_name=user_row['full_name'],
            email=user_row['email'],
            password_hash=user_row['password_hash'],
            is_verified=user_row['is_verified'],
            profile_image=user_row['profile_image'],
            phone=user_row['phone'],
            bio=user_row['bio'],
            address=user_row['address'],
            created_at=user_row['created_at']
        )
    return None

def create_user(full_name, email, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (full_name, email, password_hash, is_verified) VALUES (%s, %s, %s, %s) RETURNING id",
            (full_name, email, password_hash, False)
        )
        user_id = cur.fetchone()[0]
        return user_id
    finally:
        cur.close()
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_row = cur.fetchone()
        return get_user_object(user_row)
    finally:
        cur.close()
        conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_row = cur.fetchone()
        return get_user_object(user_row)
    finally:
        cur.close()
        conn.close()

def verify_user(email):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET is_verified = TRUE WHERE email = %s", (email,))
    finally:
        cur.close()
        conn.close()

def update_profile(user_id, full_name, phone, bio, address):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE users SET full_name = %s, phone = %s, bio = %s, address = %s WHERE id = %s",
            (full_name, phone, bio, address, user_id)
        )
    finally:
        cur.close()
        conn.close()

def update_profile_image(user_id, filename):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET profile_image = %s WHERE id = %s", (filename, user_id))
    finally:
        cur.close()
        conn.close()
