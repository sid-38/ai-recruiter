import os
import time
import uuid
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import ml

UPLOAD_FOLDER = './uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data_store = {}
  
@app.route('/', methods = ['GET', 'POST']) 
def home(): 
    if(request.method == 'GET'): 
        data = "hello world"
        return jsonify({'data': data}) 

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request)
        if 'file' not in request.files:
            return('No file part')
            # return redirect(request.url)
        file = request.files['file']

        role = request.form['role']
        print(request.form)
        print(role)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return('No selected file')
            # flash('No selected file')
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(time.time())+filename)
            file.save(file_path)
            recruiter = ml.AIRecruiter(file_path, role)
            new_id = str(uuid.uuid4())
            data_store[new_id] = {"recruiter":recruiter}
            questions = recruiter.generate_questions()
            response = jsonify({"id":new_id , "questions":questions})
            # TODO: Change CORS policy to be more restrictive
            # response.headers.add('Access-Control-Allow-Origin', '*')
            return response
            # return redirect(f"/submit_answers/{new_id}")

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
  
@app.route('/submit_answers/<rec_id>', methods=['GET','POST'])
def submit_answers(rec_id):
    if request.method=='POST':
        # req_json = request.get_json()
        answers = ""
        for i in request.form:
            answers += f"{i}. {request.form[i]}\n"
        print(answers)
        # answers = request.form['answers']
        # IF KEY DOES NOT EXIST
        # rec_id = req_json['id']
        recruiter = data_store[rec_id]['recruiter']
        score_analysis = recruiter.generate_score(answers) 
        os.remove(recruiter.file_path)
        del data_store[rec_id]
        print(score_analysis)
        return score_analysis
    if request.method=='GET':
        questions = data_store[rec_id]['recruiter'].questions
        question_text = ""
        for i, question in enumerate(questions):
           question_text += f"{i}. {question}\n"
        return f'''
        <!doctype html>
        <title>Submit Answers</title>
        {question_text}
        <form action="/submit_answers/{rec_id}" method=post enctype=multipart/form-data>
          <textarea rows="8" cols="100" name=answers></textarea>
          <input type=submit value=Upload>
        </form>
        '''

# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 
