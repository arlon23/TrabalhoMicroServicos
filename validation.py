from flask import jsonify, make_response
import json, helpers
from werkzeug.utils import secure_filename
# from main import allowed_file
# from werkzeug.utils import secure_filename

def validateCreationData(request):

    is_valid = True
    errors = dict()

    if 'files' in request.files:
        files = request.files.getlist('files')

        for file in files:
            filename = secure_filename(file.filename)
            if file and helpers.allowed_file(filename):
                continue
            else:
                errors[filename] = 'File type is not allowed'

    if 'files' not in request.files:
        is_valid = False
        errors['files'] = "This is a required field"
    if ('post_id' not in request.form):
        is_valid = False
        errors['post_id'] = "This is a required field"
    if ('files' in request.form):
        is_valid = False
        errors['files'] = "It must be a file"
    
    if(is_valid == False):
        response = make_response(jsonify(errors))
        response.status_code = 400
        
    
    return True if is_valid else response
