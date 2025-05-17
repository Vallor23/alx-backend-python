import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import csv
import uuid

load_dotenv()

# Connect to Mysql server
def connect_db() :
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        print('Connected to MySQL server')
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
# creates the database if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created")
    except Error as e:
        print(f"Error creating database: {e}")
        
# connects the the ALX_prodev database in MYSQL
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password='MYSQL_PASSWORD',
            database=os.getenv('MYSQL_PASSWORD')
        )
        print("Connected to ALX_prodev database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    
# create a table user_data if it does not exists
def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data(
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
        """
        cursor.execute(create_table_query)
        print("Table user_table created")
    except Error as e:
         print(f"Error creating table: {e}")
        
# Inserts csv data in the database if it does not exist
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        
        insert_query = """
            INSERT INTO user_data(user_id, name, email, age)
            VALUES(%s, %s, %s, %s)
        """
        
        for row in data:
            print(f"DEBUG ROW: {row}")
            name, email, age = row
            cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s", (email,))
            if cursor.fetchone()[0] == 0:
                user_id = str(uuid.uuid4())
                cursor.execute(insert_query,(user_id, name, email, int(age)))
                print(f"Inserted: {name}, {email}, {age}")
            else:
                print(f"Skipped (email esists): {email}")
                
        connection.commit()
        print("Data insertion completed.")
    except Error as e:
        print(f'Error inserting data: {e}')
        
# Read csv data
def read_csv(filepath):
    data = []
    with open(filepath,newline= '') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) >= 3:
                data.append((row[0],row[1], row[2]))
    return data

# Main script flow
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()
        
db_conn = connect_to_prodev()
if db_conn:
    create_table(db_conn)
    csv_data = read_csv("./user_data.csv")
    insert_data(db_conn, csv_data)
    db_conn.close()
    