import os
import time
import uuid
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import ml

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
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
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
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
            recruiter = ml.MockAIRecruiter(file_path)
            new_id = str(uuid.uuid4())
            data_store[new_id] = {"recruiter":recruiter}
            questions = recruiter.generate_questions()
            # return jsonify({"id":new_id , "questions":questions})
            return redirect(f"/submit_answers/{new_id}")

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
        answers = request.form['answers']
        # IF KEY DOES NOT EXIST
        # rec_id = req_json['id']
        recruiter = data_store[rec_id]['recruiter']
        score_analysis = recruiter.generate_score(answers) 
        os.remove(recruiter.file_path)
        del data_store[rec_id]
        return score_analysis
    if request.method=='GET':
        questions = data_store[rec_id]['recruiter'].questions
        return f'''
        <!doctype html>
        <title>Submit Answers</title>
        {questions}
        <form action="/submit_answers/{rec_id}" method=post enctype=multipart/form-data>
          <textarea rows="8" cols="100" name=answers></textarea>
          <input type=submit value=Upload>
        </form>
        '''

# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 
