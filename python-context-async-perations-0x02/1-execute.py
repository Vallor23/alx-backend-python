import mysql.connector
from mysql.connector import Error
import os
from dotenv  import load_dotenv

load_dotenv()
class ExecuteQuery:
    def __init__(self, host, database, user, password, query, params=None):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None
        
    def __enter__(self):
        try:
            self.conn = mysql.connector.connect()
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.query, self.params)
            # For SELECT queries, fetch results immediately
            if self.query.strip().upper().startswith('SELECT'):
                self.results = self.cursor.fetchall()
            return self
        except Error as e:
            raise Exception (f"Failed to execute query: {e}")
        
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.conn and self.conn.is_connected():
                if exc_type == None:
                    self.conn.commit() #Commit changes for none SELECT queries
                else:
                    self.conn.rollback #Rollback an error
            self.cursor.close()
            self.conn.close()
        except Error as e:
            raise Exception(f"Error closing database connection: {e}")
        finally:
            self.cursor = None
            self.conn = None
                
#Example usage
def main():
    try:
        with ExecuteQuery(
            host= os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE'),
            query= "SELECT * FROM users WHERE age > ?",
            params= (25)
        ) as results:
            for row in results:
                print(row)
    except Exception as e:
        print(f"Error: {e}")
            