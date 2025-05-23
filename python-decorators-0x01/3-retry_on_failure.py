import time
import sqlite3 
from functools import wraps

def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        
        try:
            return func(conn, *args,** kwargs)
        finally:
            conn.close()
    return wrapper     

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            
            while attempts < retries:
                try:
                    return func(*args,** kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        time.delay()
                    else:
                        print("[RETRY] All attempts failed.")
                        raise
        return wrapper
    return decorator                        
            
@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)