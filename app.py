import os
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'fit'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

def allowed_files(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Test(Resource):
    def get(self):
        return {'test': 'test'}

    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}
        
        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'data': 'success'}

api.add_resource(Test, '/')
