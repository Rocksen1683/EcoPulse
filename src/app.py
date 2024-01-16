from flask import Flask, current_app, flash, request, redirect, send_file, send_from_directory, url_for, jsonify, make_response
from flask_cors import CORS, cross_origin
from openai import AuthenticationError
import uuid

app = Flask(__name__)
cors = CORS(app, origins="*")
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_ORIGINS'] = '*'

from idea_evaluator import *

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
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
        fid = str(uuid.uuid4())
        filename = fid + ".csv"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("File saved @ ", os.path.join(app.config['UPLOAD_FOLDER'], filename))
    evaluator = IdeaEvaluator(fid, request.form['apiKey'])
    try:
        outfname = evaluator.baseline_model()
    except AuthenticationError:
        return (jsonify({'error': 'Invalid API Key'}), 400)
    categories = evaluator.populate_categories()
    barhtml = evaluator.bar_visualization()

    return jsonify({'filename': outfname, 'barhtml': barhtml, 'fid': fid, 'categories': categories})

@app.route('/api/user-predict', methods=['POST'])
def user_predict():
    try:
        evaluator = IdeaEvaluator(request.form['fid'], request.form['apiKey'])
        evaluator.user_model(request.form['userInfo'], request.form['userSector'])
        evaluator.evaluateAdditionalMetrics()
        evaluator.calculateScore()
        filteroutfname = evaluator.filter_categories(evaluator.user_model_data,request.form['category'])
        useroutfname = evaluator.export_user_model()
    except AuthenticationError:
        return (jsonify({'error': 'Invalid API Key'}), 400)
    return jsonify({'filename': useroutfname, 'filteroutfname': filteroutfname})
    

@app.route('/api/download/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(current_app.root_path, 'outs')
    print(uploads)
    print(filename)
    return send_from_directory(uploads, path=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
