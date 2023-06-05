from flask import Flask, jsonify, make_response, request
from werkzeug.utils import secure_filename
import json, time, random, os, mysql.connector, helpers
from validation import badWordsValidation, validateCreationData
from flasgger import Swagger, swag_from

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
mycursor.execute("CREATE TABLE IF NOT EXISTS files ( id int unsigned NOT NULL AUTO_INCREMENT, post_id int unsigned NOT NULL, path varchar(255) NOT NULL, filename varchar(255) NOT NULL,PRIMARY KEY (id))")

# mycursor.execute("""ALTER TABLE file_api.files 
# CHANGE COLUMN post_id post_id int NOT NULL"""
# )

# Close the cursor and database connection
mycursor.close()
mydb.close()

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

swagger = Swagger(app)
swagger.title = "Microservices Files API"
swagger.description = "Descrição da minha API"
swagger.version = "1.0"

@app.route('/upload', methods=['POST'])
@swag_from('swagger_definitions/microservices_files_api_definition.yml')
def upload_file():
    validation = validateCreationData(request)
    if(validation == True):
        mydb = mysql.connector.connect(
            host="localhost",
            user="user",
            password="user",
            database="file_api"
        )
        mycursor = mydb.cursor()
        
        files = request.files.getlist('files')

        messages = dict()

        for file in files:

            originalFilename = secure_filename(file.filename)

            folder_type = helpers.file_type(originalFilename)

            timestamp = str(int(time.time()))
            random_number = str(random.randint(1000, 9999))

            filename = timestamp + '_' + random_number + "." + folder_type['ext']

            absolutePath = app.config['UPLOAD_FOLDER']+folder_type['path']
            
            file.save(os.path.join(absolutePath, filename))

            sql = "INSERT INTO files (post_id,path,filename) VALUES (%s, %s, %s)"
            val = (request.form['post_id'], absolutePath, filename)

            mycursor.execute(sql, val)

            mydb.commit()

            file_id = mycursor.lastrowid

            messages[file_id] = {
                'file_id': file_id,
                'path': absolutePath,
                'filename': filename,
                'post_id': request.form['post_id']
            }
            print("The ID of the last inserted row is:", mycursor.lastrowid)
        mydb.close()

        response = make_response(jsonify(messages))
        response.status_code = 200

        return response
    else:
        return validation
    
@app.route('/list/<post_id>', methods=['GET'])
@swag_from('swagger_definitions/microservices_files_api_definition.yml')
def list_post(post_id):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="user",
            password="user",
            database="file_api"
        )

        mycursor = mydb.cursor()

        sql = "SELECT * FROM files WHERE files.post_id = %s"

        mycursor.execute(sql, (post_id,))  # Executar a consulta antes de chamar fetchall()

        result = mycursor.fetchall()
        
        mydb.close()

        rows = []
        for row in result:
            rows.append({
                'id': row[0],
                'post_id': row[1],
                'path': row[2],
                'file_name': row[3]
            })

        return jsonify(rows)
    except:
        return jsonify({'error': 'Something went wrong, please contact admin support'}), 500

@app.route('/list', methods=['GET'])
@swag_from('swagger_definitions/microservices_files_api_definition.yml')
def list_all():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="user",
            password="user",
            database="file_api"
        )

        mycursor = mydb.cursor()

        sql = "SELECT * FROM files"

        mycursor.execute(sql)  # Executar a consulta antes de chamar fetchall()

        result = mycursor.fetchall()
        
        mydb.close()

        if len(result) == 0:
            return jsonify({'message': 'A tabela está vazia'})

        rows = []
        for row in result:
            rows.append({
                'id': row[0],
                'post_id': row[1],
                'path': row[2],
                'file_name': row[3]
            })

        return jsonify(rows)
    except:
        return jsonify({'error': 'Something went wrong, please contact admin support'}), 500

@app.route('/delete/<file_id>', methods=['DELETE'])
@swag_from('swagger_definitions/delete_file.yml')
def delete_file(file_id):
    print(file_id is not None)
    if (file_id):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="user",
                password="user",
                database="file_api"
            )
            mycursor = mydb.cursor()

            sql = "DELETE FROM files WHERE id = %s"
            val = (file_id,)

            mycursor.execute("SELECT CONCAT(path, '/', filename) as test FROM files WHERE id = %s", val)

            absolutePath = (mycursor.fetchall()[0])[0]

            os.remove(absolutePath)
            mycursor.execute(sql, val)

            mydb.commit()

            mydb.close()
            return jsonify({'message': 'Image deleted successfully'}), 200
        except OSError:
            return jsonify({'error': 'Image not found'}), 404
        except:
            return jsonify({'error': 'Something went wrong, please contact admin support'}), 500

    return jsonify({'error' : 'Missing required parameter: file_id'}), 400

if __name__ == '__main__':
    app.run(debug=True)