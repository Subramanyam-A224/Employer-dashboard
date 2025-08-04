import pymysql

def db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="subbu@123",
        database="employee_db"
    )
