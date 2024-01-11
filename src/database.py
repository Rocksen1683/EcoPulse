# app.py

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create SQLite database and table
conn = sqlite3.connect('eco_pulse.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem TEXT,
        solution TEXT,
    )
''')

conn.commit()
conn.close()
