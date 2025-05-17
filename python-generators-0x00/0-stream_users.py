import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    for row in cursor:
        yield row
    
    cursor.close()
    connection.close()