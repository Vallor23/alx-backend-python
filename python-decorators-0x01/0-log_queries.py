import sqlite3
import functools

#### decorator to lof SQL queries

def log_queries(func):
    def wrapper(*args, **kwargs):
        if args:
            sql = args[0]
        else:
            None
        print(f"[LOG] Executing SQL: {sql}")
        
        result = func(*args, **kwargs)
        
        print(f"[LOG] Query result: {result}")
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
        