import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:
        batch.append(row)
        
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield(batch)
    cursor.close()
    connection.close()
    
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users = (user for user in batch if int(user['age'])> 25)
        yield filtered_users