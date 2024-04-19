from flask import Flask, render_template, request, jsonify
from pulldata import get_query
from responses import get_Chat_response
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('chatbot.html')


@app.route("/predict", methods=["GET","POST"])

def predict():
    text = request.get_json().get("message")
    level = request.get_json().get("state")
    response,state = get_Chat_response(level,text)
    message = {'response':response,'state':state}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)