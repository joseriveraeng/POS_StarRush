import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

def get_database_connection():
    try:
      connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
      )
      return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def star_init():
    connect = get_database_connection()
    if connect is None:
        print("The connection could not be established.")
        return
        
    cursor = connect.cursor()
    
    try:
        with open("sql/init.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

       
        cursor.execute(sql_script)

        while cursor.nextset():
            pass

        connect.commit()
        print("Database successfully initialized")
        
    except mysql.connector.Error as err:
        print(f"Error starting the database: {err}")
    finally:
        cursor.close()
        connect.close()

if __name__ == "__main__":
    star_init()