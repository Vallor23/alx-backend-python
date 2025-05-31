import mysql.connector
from mysql.connector import Error
import os
from dotenv  import load_dotenv

load_dotenv()
class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        
    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database,
                user = self.database,
                password = self.password
            )
            self.cursor = self.connection.cursor()
            return self.cursor
        except Error as e:
            print(f"Failed to connect to database: {e}")
            raise
        
    def __exit__(self,  exc_type, exc_value, traceback):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                self.cursor.close()
                self.connection.close()
                
def main():
    with DatabaseConnection(
        host= os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    ) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            yield row

if __name__ == "__main__":
    main()