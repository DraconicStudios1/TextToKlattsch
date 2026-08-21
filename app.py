from flask import Flask, render_template, request, send_file
from zipfile import ZipFile
import io
import os
import runpy
import sys
import subprocess

app = Flask(__name__)

script_to_run = 'arpabet/convert_arpabet.py'
file_path1 = 'output.txt'

sys.argv = [script_to_run, "--file", file_path1]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    # 1. Get user input from the HTML form
    user_input = request.form['text_input']
    bass_in = request.form['bass_input']
    
    # 2. Write the input to a text file and convert the text to Arpabet
    file_path = 'output.txt'
    with open(file_path, 'w') as file:
        file.write(user_input)
    runpy.run_path(script_to_run, run_name="__arpa__")
    # 3. Force the browser to download the text file
    arpa_file_path = 'outputARPA.txt'
    with open(arpa_file_path, 'r') as file:
        doc = file.read()
    doc_list = list(doc)
    idx = doc_list.index('|')
    for i, char in enumerate(doc_list):
        if char == '{':
            doc_list[i] = ''
        if char == '}':
            doc_list[i] = ''
        if char == '0':
            doc_list[i] = ''
        if char == '1':
            doc_list[i] = ''
        if char == '2':
            doc_list[i] = ''
        if char == ',':
            doc_list[i] = ' p500'
        if char == '.':
            doc_list[i] = ''

    for i in range(idx + 1):
        doc_list[i] = ''

    cleaned_arpa = "".join(doc_list)
    with open(arpa_file_path, 'w') as file:
        file.write(cleaned_arpa)

    subprocess.run("npx klattsch " + '"' + bass_in + " " + cleaned_arpa + '"', shell=True)
    klattsch_file = 'klattsch.wav'

    file_paths = [
        klattsch_file,
        arpa_file_path
    ]
    
    zip_buffer = io.BytesIO()
    
    with ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in file_paths:
            if os.path.exists(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
                
    zip_buffer.seek(0)
    
    # 5. Send the stream back as a downloadable attachment
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='generated_assets.zip'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
