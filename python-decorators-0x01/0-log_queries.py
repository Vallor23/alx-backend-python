import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

def log_queries(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if args:
            sql = args[0]
        else:
            None
        print(f"[{timestamp}] [LOG] Executing SQL: {sql}")
        
        result = func(*args, **kwargs)
        
        print(f"[{timestamp}] [LOG] Query result: {result}")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
        