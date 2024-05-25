import gradio as gr
import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage
import pandas as pd
import json

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_API_KEY"] = api_key

def prepare_message(document, annotations, output_columns):
    message = f"Generate synthetic data based on the following document and annotations:\nDocument: {document}\n"
    for text, column in annotations:
        message += f"Annotate text '{text}' as '{column}'.\n"
    message += f"Output columns: {', '.join(output_columns)}"
    return message

def send_request_to_llm(document, annotations_str, output_columns_str):
    annotations = [tuple(annot.split(': ')) for annot in annotations_str.split('\n') if annot]
    output_columns = output_columns_str.split(", ")
    n_rows = 10
    system_prompt = "Prepare synthetic data generation model."
    user_query = prepare_message(document, annotations, output_columns)
    messages = [
        # ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="system", content=f'''
                    Generate some dummy data with the information given,
                    to create a dataset for a Chat AI model training.
                    For a given input, {n_rows} output should be given,
                    and each row should be diverse from one another.
                    normal chat AI dataset, which means few of the 
                    columns should involve conversation.
                    The data should be in a dict format.
                    If context length limit is reached,
                    do not end with incomplete dict.
                    Respond only with a string
                    of dict data with {n_rows} rows of data.
                    '''),
        ChatMessage(role="user", content=user_query)
    ]
    gemini = Gemini(model_name="models/gemini-1.0-pro", max_tokens=30720, temperature=1)
    response = str(gemini.chat(messages)).replace('assistant:','')
    return response


def generate_and_save(document, annotations, output_columns):
    response = send_request_to_llm(document, annotations, output_columns)
    print('0'*100)
    print(response)
    data = json.loads(response)
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
    return df

with gr.Blocks() as app:
    with gr.Row():
        document = gr.Textbox(label="Input Document")
        annotations = gr.Textbox(label="Annotations (Format: 'text: column')", placeholder="Enter each annotation on a new line")
        output_columns = gr.Textbox(label="Output Columns (Comma-separated)")
    generate_button = gr.Button("Generate Dataset")
    output_table = gr.Dataframe()
    generate_button.click(generate_and_save, inputs=[document, annotations, output_columns], outputs=output_table)

app.launch()
