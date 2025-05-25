import mysql.connector
from mysql.connector import Error

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