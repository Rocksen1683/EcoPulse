from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from openai import AuthenticationError
import asyncio
import websockets
import uuid
import os
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

async def send_evaluation():
    uri = "ws://localhost:5000/ws/"  # Adjust the URL based on your server's address
    async with websockets.connect(uri) as websocket:
        await websocket.send("Evaluate")
        response = await websocket.recv()
        print(response)

@app.route('/ws/')
@cross_origin()
async def websocket_handler( ws):
    print("WebSocket connection established")
    
    try:
        message = await ws.recv()
        if message == "Evaluate":
            # Perform evaluation or any other processing based on filename and api_key
            await ws.send("Evaluation completed successfully")
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")


async def send_evaluation():
    uri = "ws://localhost:5000/ws/"  # Adjust the URL based on your server's address
    async with websockets.connect(uri) as websocket:
        await websocket.send("Evaluate")
        response = await websocket.recv()
        print(response)

@app.route('/ws/')
async def websocket_handler( ws):
    print("WebSocket connection established")
    
    try:
        message = await ws.recv()
        if message == "Evaluate":
            # Perform evaluation or any other processing based on filename and api_key
            await ws.send("Evaluation completed successfully")
    except websockets.exceptions.ConnectionClosedError:
        print("WebSocket connection closed")


if __name__ == '__main__':
    app.run(debug=True)
    start_server = websockets.serve(websocket_handler, "localhost", 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    print("Server started")
    send_evaluation()
