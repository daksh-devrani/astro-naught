import json
import random
import string
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
IS_POSTGRES = DATABASE_URL is not None and DATABASE_URL.startswith("postgres")

if IS_POSTGRES:
    import psycopg2
    import psycopg2.extras
else:
    import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "reports.db")

def get_connection():
    if IS_POSTGRES:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    if IS_POSTGRES:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shared_reports (
                short_code TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                input_payload TEXT NOT NULL,
                result_payload TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                unique_views INTEGER DEFAULT 0,
                source_report_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_viewed_at TIMESTAMP
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shared_reports (
                short_code TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                input_payload TEXT NOT NULL,
                result_payload TEXT NOT NULL,
                views INTEGER DEFAULT 0,
                unique_views INTEGER DEFAULT 0,
                source_report_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_viewed_at TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_report(report_type: str, input_payload: dict, result_payload: dict, source_report_code: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Generate unique short code
    while True:
        short_code = generate_short_code()
        if IS_POSTGRES:
            cursor.execute("SELECT short_code FROM shared_reports WHERE short_code = %s", (short_code,))
        else:
            cursor.execute("SELECT short_code FROM shared_reports WHERE short_code = ?", (short_code,))
            
        if not cursor.fetchone():
            break

    if IS_POSTGRES:
        cursor.execute("""
            INSERT INTO shared_reports 
            (short_code, type, input_payload, result_payload, source_report_code, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            short_code, 
            report_type, 
            json.dumps(input_payload), 
            json.dumps(result_payload), 
            source_report_code,
            datetime.utcnow()
        ))
    else:
        cursor.execute("""
            INSERT INTO shared_reports 
            (short_code, type, input_payload, result_payload, source_report_code, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            short_code, 
            report_type, 
            json.dumps(input_payload), 
            json.dumps(result_payload), 
            source_report_code,
            datetime.utcnow().isoformat()
        ))
        
    conn.commit()
    conn.close()
    return short_code

def get_report(short_code: str, increment_view: bool = True):
    conn = get_connection()
    
    if IS_POSTGRES:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM shared_reports WHERE short_code = %s", (short_code,))
    else:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shared_reports WHERE short_code = ?", (short_code,))
        
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
        
    # Increment views
    if increment_view:
        if IS_POSTGRES:
            cursor.execute("""
                UPDATE shared_reports 
                SET views = views + 1, last_viewed_at = %s 
                WHERE short_code = %s
            """, (datetime.utcnow(), short_code))
        else:
            cursor.execute("""
                UPDATE shared_reports 
                SET views = views + 1, last_viewed_at = ? 
                WHERE short_code = ?
            """, (datetime.utcnow().isoformat(), short_code))
        conn.commit()
        
    conn.close()
    
    return {
        "short_code": row["short_code"],
        "type": row["type"],
        "input_payload": json.loads(row["input_payload"]),
        "result_payload": json.loads(row["result_payload"]),
        "views": row["views"] + (1 if increment_view else 0),
        "created_at": row["created_at"],
        "last_viewed_at": row["last_viewed_at"]
    }
