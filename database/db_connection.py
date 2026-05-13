import psycopg2
from psycopg2.extras import DictCursor
from config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    conn.autocommit = True
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Let's create the users table if it doesn't already exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id            SERIAL PRIMARY KEY,
            full_name     VARCHAR(255) NOT NULL,
            email         VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_verified   BOOLEAN DEFAULT FALSE,
            profile_image TEXT,
            phone         VARCHAR(20),
            bio           TEXT,
            address       TEXT,
            created_at    TIMESTAMP DEFAULT NOW()
        );
    ''')
    cur.close()
    conn.close()
