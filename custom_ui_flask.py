from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage
import json
import pandas as pd

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    document = data['document']
    annotations = data['annotations']  # List of dicts [{'text': 'some text', 'class': 'some class'}, ...]
    output_columns = data['output_columns']
    response = send_request_to_llm(document, annotations, output_columns)
    return jsonify(response)

def send_request_to_llm(document, annotations, output_columns):
    annotations_formatted = [(annot['text'], annot['class']) for annot in annotations]
    output_columns_str = ", ".join(output_columns)
    n_rows = 10
    user_query = prepare_message(document, annotations_formatted, output_columns)
    messages = [
        ChatMessage(role="user", content=user_query)
    ]
    gemini = Gemini(model_name="models/gemini-1.0-pro", max_tokens=30720, temperature=1)
    response = str(gemini.chat(messages)).replace('assistant:', '')
    return json.loads(response)

def prepare_message(document, annotations, output_columns):
    message = f"Generate synthetic data based on the following document and annotations:\nDocument: {document}\n"
    for text, column in annotations:
        message += f"Annotate text '{text}' as '{column}'.\n"
    message += f"Output columns: {', '.join(output_columns)}"
    return message

if __name__ == '__main__':
    app.run(debug=True)
