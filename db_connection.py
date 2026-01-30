import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # XAMPP default (leave empty)
            database="serenistay_db"
        )
        return conn
    except mysql.connector.Error as err:
        print("Database Error:", err)
        return None
