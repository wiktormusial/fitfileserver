import os
from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
import fitparse


UPLOAD_FOLDER = 'files/'
ALLOWED_EXTENSIONS = {'fit'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)


def get_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

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
            file.save(get_path(filename))
            fitfile = fitparse.FitFile(get_path(filename))
            
            coords = [] 
            response = {}
            counter = 0
            for record in fitfile.get_messages("record"):
                for data in record:
                    if data.name == 'position_lat':
                        x = round(data.value * (180 / 2**31), 5)
                    if data.name == 'position_long':
                        y = round(data.value * (180 / 2**31), 5)
                
                counter = counter + 1
                if counter % 10 == 0:
                    coords.append({'x': x, 'y': y}) 
                
                
            response['coords'] = coords

            return {'data': response}

api.add_resource(Test, '/')
