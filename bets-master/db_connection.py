import mysql.connector #pip install mysql-connector-python
from mysql.connector import Error


def get_connection():
    """get connection to the database, return the connection descriptor or error"""
    try:
        connection = mysql.connector.connect(host='sql7.freesqldatabase.com',
                                             database='sql7300330',
                                             user='sql7300330',
                                             password='VeSxtzWjTK')
        return connection
    except Error as e :
        print ("Error while connecting to MySQL", e)
        return 1



def get_connection2():
    try:
        connection = mysql.connector.connect(host='sql7.freesqldatabase.com',
                             database='sql7300330',
                             user='sql7300330',
                             password='VeSxtzWjTK')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ",db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print ("Your connected to - ", record)
    except Error as e :
        print ("Error while connecting to MySQL", e)
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

