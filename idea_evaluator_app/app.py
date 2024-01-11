import csv
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

from ../idea_evaluator import *

@app.route('/api/predict', methods=['POST'])
def predict():
    evaluator = IdeaEvaluator("../data/AI_EarthHack_Dataset_Small.csv")
    evaluator.run_evaluator()
    test = "test"
    return {jsonify({'test': test})}

if __name__ == '__main__':
    app.run(debug=True)