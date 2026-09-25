from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from transcribe import get_subtitles
import os

app = Flask(__name__)

allowed_video_type = {'mp4', 'avi', 'mov', 'wmv', 'ogg', 'webm', 'mkv', 'flv'}

def valid_filetype(filename:str):
    #Checks if filetype is valid by splitting the filename into two.  
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower() in allowed_video_type

@app.route('/', methods=['GET'])
def index():
    #Returns the home page.
    return render_template('index.html')

@app.route('/video', methods=['POST'])
def video():
    if 'video' not in request.files:
        #Checks if a video is uploaded or not
        flash('No file found')
         
    #Retrieves uploaded file
    file = request.files['video']

    if file.filename == '':
        #Checks if user uploads a file.
        flash('No file uploaded')
        
    if file and valid_filetype(file.filename):
        #Checks if filetype is safe and saves it into resources/files.
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index', value=filename))
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.config.from_pyfile('../config.py')
    app.run(debug=True)