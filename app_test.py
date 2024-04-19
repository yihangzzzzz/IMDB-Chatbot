from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello, World"

if __name__ == '__main__':
    app.run(debug=True)