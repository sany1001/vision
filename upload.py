from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'imageFile' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['imageFile']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y.%m.%d_%H:%M:%S_')
            filename = timestamp + file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            return jsonify({'success': True, 'message': 'File uploaded successfully'})
        else:
            return jsonify({'error': 'Invalid file type'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
