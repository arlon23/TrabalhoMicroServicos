from flask import jsonify, make_response
import json, helpers
from werkzeug.utils import secure_filename
from helpers import BAD_WORDS, file_type
import PyPDF4
from io import BytesIO
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
                
                if (badWordsValidation(file) is True):
                    
                    errors[filename] = 'File content has bad words'
                    is_valid = False

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

# def pdfContent(file):
#     # stringVerifier(file.stream.read(), BAD_WORDS)
#     # file_stream = BytesIO()
#     # file_stream.write(file.read())
#     # file_stream.seek(0)

#     # stringVerifier(file.read().decode('utf-8'))

#     content = ""

#     pdf_reader = PyPDF4.PdfFileReader(file)

#     # Iterate over each page in the PDF and extract the text
#     for page in pdf_reader.pages:
#         content += page.extractText()

#     # pdfReader = PyPDF4.PdfFileReader(file.stream)
    
#     # for pageNumber in range(pdfReader.numPages):
#     #     pdf_page = pdfReader.getPage(pageNumber)
#     #     content += pdf_page.extractText()
#     print(content)
#     return content

def stringVerifier(text, strings):
    for word in strings:
        if word in text:
            return True
    return False

# filename - nome do arquivo + extensao
def badWordsValidation(file):
    filename = secure_filename(file.filename)

    if (file_type(filename)['ext'] == 'txt'):
        return True if stringVerifier(file.read().decode('utf-8'), BAD_WORDS) else False
    
    return False