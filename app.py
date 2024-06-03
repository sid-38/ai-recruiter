import os
import time
import uuid
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import ml
import json

with open("./config.json", 'r') as f:
    CONFIG = json.load(f)

# UPLOAD_FOLDER = './uploads'
# UPLOAD_FOLDER = config['UPLOAD_FOLDER']

if not os.path.exists(CONFIG["UPLOAD_FOLDER"]):
    os.makedirs(CONFIG["UPLOAD_FOLDER"])

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
# Configure CORS to be more restrictive
CORS(app)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Will contain the state to map answers to the questions
data_store = {}
  
def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return('No file part', 400)

        file = request.files['file']
        role = request.form['role']

        if file.filename == '':
            return('No selected file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(CONFIG['UPLOAD_FOLDER'], str(time.time())+filename)
            file.save(file_path)

            recruiter = ml.MockAIRecruiter(file_path, role)
            # This ID is used by the backend to "remember" when the user submits the answer
            new_id = str(uuid.uuid4())
            data_store[new_id] = {"recruiter":recruiter}
            questions = recruiter.generate_questions()
            response = jsonify({"id":new_id , "questions":questions})
            return response

    return "Method not supported", 405
  
@app.route('/submit_answers/<rec_id>', methods=['POST'])
def submit_answers(rec_id):
    if request.method=='POST':

        answers = ""
        for i in request.form:
            answers += f"{i}. {request.form[i]}\n"

        try:
            recruiter = data_store[rec_id]['recruiter']
        except:
            return "Key does not exist", 400

        score_analysis = recruiter.generate_score(answers) 
        os.remove(recruiter.file_path)
        del data_store[rec_id]
        return score_analysis

# driver function 
if __name__ == '__main__': 
    app.run(host=CONFIG['BACKEND_HOST'], port=CONFIG['BACKEND_PORT'], debug = True) 
