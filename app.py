from flask import *
from werkzeug.utils import secure_filename
import json, time, random, os, helpers
from validation import validateCreationData
from mysqlHelper import *
# from flask import Flask, jsonify
import requests

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USERS = {"user-2": 2, "user-0": 0}
USER_KEYS = ["user-2", "user-0"]
AUTHENTICATION_API_URL="http://localhost:8000"

@app.route('/me', methods=['GET'])
def test():
    response = dict()
    message = dict()
    message['id'] = 123
    message['name'] = 'John Doe'
    message['registration'] = 'ABC123'
    message['email'] = 'johndoe@example.com'
    message['email_verified_at'] = ''
    message['admin'] = True
    message['created_at'] = '2023-07-01T10:00:00Z'
    message['updated_at'] = '2023-07-01T12:00:00Z'
    # response['data'] = message
    response = make_response(jsonify(message))
    response.status_code = 200
    return response

@app.route('/files-api', methods=['POST'])
def upload_file():
    # AUTHENTICATION_API_URL+'/me'
    authResponse = requests.get('http://127.0.0.1:5000/me')

    if (authResponse.status_code == 200):
        user = (authResponse.json())['id']
    else:
        error = dict()
        message = dict()
        message['error'] = 'Invalid User'
        error['data'] = message
        response = make_response(jsonify(error))
        response.status_code = 403
        return response
    
    validation = validateCreationData(request)
    if(validation == True):
        mydb = connectDatabase()

        mycursor = mydb.cursor()
        
        files = request.files.getlist('files')

        # messages = dict()
        arrayList = []
        # count = 0
        for file in files:
            
            originalFilename = secure_filename(file.filename)

            folder_type = helpers.file_type(originalFilename)

            timestamp = str(int(time.time()))
            random_number = str(random.randint(1000, 9999))

            filename = timestamp + '_' + random_number +'.'+folder_type['ext']

            absolutePath = app.config['UPLOAD_FOLDER']+folder_type['path']
            
            file.save(os.path.join(absolutePath, filename))

            sql = "INSERT INTO files (post_id,path,filename,user_id) VALUES (%s, %s, %s, %s)"
            val = (request.form['post_id'], absolutePath, filename, user)

            mycursor.execute(sql, val)

            mydb.commit()

            file_id = mycursor.lastrowid

            # messages[count] = {
            #     'image_id': file_id,
            #     'path': absolutePath,
            #     'filename': filename,
            #     'post_id': request.form['post_id'],
            #     'user_id': request.form['post_id']
            # }
            arrayList.append({
                'image_id': file_id,
                'path': absolutePath,
                'filename': filename,
                'post_id': int(request.form['post_id']),
                'user_id': user
            })
            
            # print("The ID of the last inserted row is:", mycursor.lastrowid)
        mydb.close()

        # print(arrayList)
        
        formattedResponse = {
            'data': arrayList
        }
        response = make_response(formattedResponse)
        response.status_code = 201

        return response
    else:
        return validation
    
@app.route('/files-api/<post_id>', methods=['GET'])
def list_post(post_id):
    try:
        # AUTHENTICATION_API_URL+'/me'
        authResponse = requests.get('http://127.0.0.1:5000/me')

        if (authResponse.status_code == 200):
            user = (authResponse.json())['id']
        else:
            error = dict()
            message = dict()
            message['error'] = 'Invalid User'
            error['data'] = message
            response = make_response(jsonify(error))
            response.status_code = 403
            return response
        mydb = connectDatabase()

        mycursor = mydb.cursor()

        sql = "SELECT * FROM files WHERE files.post_id = %s and files.user_id = %s"

        mycursor.execute(sql, (post_id, user,))  # Executar a consulta antes de chamar fetchall()

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

@app.route('/files-api/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    if (file_id is not None):
        try:
            # AUTHENTICATION_API_URL+'/me'
            authResponse = requests.get('http://127.0.0.1:5000/me')

            if (authResponse.status_code == 200):
                user = (authResponse.json())['id']
            else:
                error = dict()
                message = dict()
                message['error'] = 'Invalid User'
                error['data'] = message
                response = make_response(jsonify(error))
                response.status_code = 403
                return response
            
            mydb = connectDatabase()
            mycursor = mydb.cursor()

            sql = "DELETE FROM files WHERE id = %s and user_id = %s"
            val = (file_id,)

            mycursor.execute("SELECT CONCAT(path, '/', filename) as test FROM files WHERE id = %s", val)
            fetch = mycursor.fetchall()
            val = (file_id, user,)

            hasFound = len(fetch)
            
            if hasFound:
                mycursor.execute("SELECT CONCAT(path, '/', filename) as test FROM files WHERE id = %s and user_id = %s", val)
                fetch = mycursor.fetchall()
                if len(fetch):
                    absolutePath = (fetch[0])[0]
                else:
                    error = dict()
                    message = dict()
                    message['error'] = 'User is not allowed to delete this file'
                    error['data'] = message
                    response = make_response(jsonify(error))
                    response.status_code = 403
                    return response
            else:
                absolutePath = ''

            os.remove(absolutePath)
            mycursor.execute(sql, val)
            
            mydb.commit()

            mydb.close()

            data = dict()
            message = dict()
            message['message'] = 'File deleted successfully'
            data['data'] = message
            response = make_response(jsonify(data))
            response.status_code = 200
            return response
        except OSError:
            error = dict()
            message = dict()
            message['error'] = 'File not found'
            error['data'] = message
            response = make_response(jsonify(error))
            response.status_code = 404
            return response
        except Exception:
            error = dict()
            message = dict()
            message['error'] = 'Something went wrong, please contact admin support'
            error['data'] = message
            response = make_response(jsonify(error))
            response.status_code = 500
            return response
        
    error = dict()
    message = dict()
    message['error'] = 'Missing required parameter: file_id'
    error['data'] = message
    response = make_response(jsonify(error))
    response.status_code = 400
    return response

# @app.route('/files-api', methods=['GET'])
# def list_all():
#     try:
#         mydb = connectDatabase()

#         mycursor = mydb.cursor()

#         sql = "SELECT * FROM files"

#         mycursor.execute(sql)  # Executar a consulta antes de chamar fetchall()

#         result = mycursor.fetchall()
        
#         mydb.close()

#         if len(result) == 0:
#             return jsonify({'message': 'A tabela está vazia'})

#         rows = []
#         for row in result:
#             rows.append({
#                 'id': row[0],
#                 'post_id': row[1],
#                 'path': row[2],
#                 'file_name': row[3]
#             })

#         return jsonify(rows)
#     except:
#         return jsonify({'error': 'Something went wrong, please contact admin support'}), 500