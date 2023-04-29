from flask import *
from werkzeug.utils import secure_filename
import json, time, os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOCUMENTS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    print('request')
    print(request.files)
    if 'files' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    
    files = request.files.getlist('files')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            folder_type = file_type(file.filename)
            
            file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST']+folder_type, filename))

            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    

    return jsonify({'message' : 'it worked'})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_type(filename):
    print(filename)
    if (filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES):
        return '/images'
    elif (filename.rsplit('.', 1)[1].lower() in ALLOWED_DOCUMENTS):
        return '/documents'
    else:
        return ''

if __name__ == '__main__':
    app.run(debug=True)