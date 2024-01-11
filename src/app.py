from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from openai import AuthenticationError
import uuid

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from idea_evaluator import *

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + ".csv"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("File saved @ ", os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file', filename=file.filename))
    try:
        evaluator = IdeaEvaluator(f"./data/{filename}", request.form['apiKey'])
        evaluator.run_evaluator()
    except AuthenticationError:
        return (jsonify({'error': 'Invalid API Key'}), 400)
    return jsonify({'hello': 'world'})

if __name__ == '__main__':
    app.run(debug=True)