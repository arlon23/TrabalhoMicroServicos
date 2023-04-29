from flask import *
from werkzeug.utils import secure_filename
import json, time, os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="arlon",
  password="",
)

# Create a cursor object
mycursor = mydb.cursor()

# Create a new database schema
mycursor.execute("CREATE DATABASE IF NOT EXISTS file_api")

# Switch to the new database schema
mycursor.execute("USE file_api")


# Create a new table
mycursor.execute("CREATE TABLE IF NOT EXISTS files ( id int unsigned NOT NULL AUTO_INCREMENT, post_id int unsigned NOT NULL, path varchar(255) NOT NULL, filename varchar(255) NOT NULL,PRIMARY KEY (id))")

# mycursor.execute("""ALTER TABLE file_api.files 
# CHANGE COLUMN post_id post_id int NOT NULL"""
# )

# Close the cursor and database connection
mycursor.close()
mydb.close()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOCUMENTS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():

    mydb = mysql.connector.connect(
        host="localhost",
        user="arlon",
        password="",
        database="file_api"
    )
    mycursor = mydb.cursor()

    if 'files' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    
    files = request.files.getlist('files')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            folder_type = file_type(filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+folder_type, filename))

            sql = "INSERT INTO files (post_id,path,filename) VALUES (%s, %s, %s)"
            val = (request.form['post_id'], app.config['UPLOAD_FOLDER']+folder_type, filename)

            mycursor.execute(sql, val)

            mydb.commit()

            print("The ID of the last inserted row is:", mycursor.lastrowid)

            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    mydb.close()

    return jsonify({'message' : 'it worked'})

@app.route('/delete', methods=['DELETE'])
def delete_file():
    print(request.form['file_id'])

    if (request.form['file_id']):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="arlon",
                password="",
                database="file_api"
            )
            mycursor = mydb.cursor()

            sql = "DELETE FROM files WHERE id = %s"
            val = (request.form['file_id'],)

            mycursor.execute("SELECT CONCAT(path, '/', filename) as test FROM files WHERE id = %s", val)

            absolutePath = (mycursor.fetchall()[0])[0]

            os.remove(absolutePath)
            mycursor.execute(sql, val)

            mydb.commit()

            mydb.close()
            return jsonify({'message': 'Image deleted successfully'})
        except OSError:
            return jsonify({'error': 'Image not found'}), 404

    return jsonify({'message' : 'it worked'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_type(filename):
    if (filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES):
        return '/images'
    elif (filename.rsplit('.', 1)[1].lower() in ALLOWED_DOCUMENTS):
        return '/documents'
    else:
        return ''

if __name__ == '__main__':
    app.run(debug=True)