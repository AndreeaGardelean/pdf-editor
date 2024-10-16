from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from splitPdf import downloadSelected
from splitPdf import deleteSelected
import os
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-type'

"""
API for transforming an uploaded PDF file to a new PDF file that contains only the selected pages, 
as specified by the client.

POST /download: 
  Expect a file to be passed from the client as form data and an array containing the selected pages.
        
  Returns:
    - zip file containing the a new pDF file only containing the selected pages.
    - JSON response containing an error message if no file has been sent from the client.
"""
@app.route('/download', methods=["POST"])
def downloadSelectedPages():
    if request.method == "POST":
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'No file attached'})

        file = request.files['pdfFile']
        pages = json.loads(request.form['selectedPages'])        
        name = json.loads(request.form['fileName'])

        print(pages, name)

        if file.filename == '':
            return jsonify({'error': 'No file attached'})

        result = downloadSelected(file, pages, name)

        return send_file(result, as_attachment=True, download_name=f'{name}.zip', mimetype='application/zip')

"""
API for transforming an uploaded PDF file to a new PDF file that contains only the non-selected pages, 
as specified by the client.

POST /delete: 
  Expect a file to be passed from the client as form data and an array containing the selected pages.
        
  Returns:
    - zip file containing a new PDF file containing the non-selected pages.
    - JSON response containing an error message if no file has been sent from the client.
"""
@app.route('/delete', methods=["POST"])
def deleteSelectedPages():
    if request.method == "POST":
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'No file attached'})

        file = request.files['pdfFile']
        pages = json.loads(request.form['selectedPages'])        
        name = json.loads(request.form['fileName'])

        if file.filename == '':
            return jsonify({'error': 'No file attached'})

        result = deleteSelected(file, pages, name)

        return send_file(result, as_attachment=True, download_name=f'{name}.zip', mimetype='application/zip')
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)