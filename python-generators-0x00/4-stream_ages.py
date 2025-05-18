import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_user_ages():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    user_ages =[]
    for row in cursor:
        yield(row['age'])
        
    cursor.close()
    connection.close()
    
def average_user_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    if count == 0:
        return 0
    
    return total_age / count
    
print(f"Average age of users: {average_user_age()}")