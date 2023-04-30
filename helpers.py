ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOCUMENTS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_type(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    file_type = dict()

    file_type['ext'] = extension

    if (extension in ALLOWED_IMAGES):
        file_type['path'] = '/images'
    elif (extension in ALLOWED_DOCUMENTS):
        file_type['path'] = '/documents'

    return file_type