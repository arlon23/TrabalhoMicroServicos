import mysql.connector


def createSchemaAndTable():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="user",
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Create a new database schema
    mycursor.execute("CREATE DATABASE IF NOT EXISTS file_api")

    # Switch to the new database schema
    mycursor.execute("USE file_api")


    # Create a new table
    mycursor.execute("CREATE TABLE IF NOT EXISTS files ( id int unsigned NOT NULL AUTO_INCREMENT, post_id int unsigned NOT NULL, user_id int unsigned NOT NULL, path varchar(255) NOT NULL, filename varchar(255) NOT NULL,PRIMARY KEY (id))")

    # mycursor.execute("""ALTER TABLE file_api.files 
    # CHANGE COLUMN post_id post_id int NOT NULL"""
    # )

    # Close the cursor and database connection
    mycursor.close()
    mydb.close()

def connectDatabase():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="user",
        database="file_api"
    )