from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource
from resources.transcribe import Transcribe
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = Transcribe()
allowed_video_formats = {'mp4', 'avi', 'mov', 'wmv', 'ogg', 'webm', 'mkv', 'flv'}
allowed_audio_formats = {'mp3', 'wav', 'flac', 'wma', 'aac', 'aiff', 'ogg', 'midi'}

@app.route('/', methods=['GET'])
def index():
    #Returns the home page.
    return render_template('index.html')

def valid_filetype(filename:str, type:str):
    #Checks if filetype is valid by checking file extension at the end. 
    if type == 'video':
        allowed_format = allowed_video_formats
    elif type == 'audio':
        allowed_format = allowed_audio_formats
    else:
        return 'File is required'
    
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower() in allowed_format

@app.route('/video', methods=['POST'])
def video(filetype:str='video'):
    if 'video' not in request.files:
        #Checks if a video is uploaded or not
        flash('No file found')
         
    #Retrieves uploaded file
    file = request.files['video']
        
    if file and valid_filetype(file.filename, filetype):
        #Checks if filetype is safe and saves it into static/uploads.
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        subtitles = model.transcribe(path)
        return render_template('index.html', video=f'../{path}', video_subtitles=subtitles)
    
    return redirect(url_for('index'))

@app.route('/audio', methods=['POST'])
def audio(filetype:str='audio'):
    if 'audio' not in request.files:
        #Checks if audio is submitted or not.
        flash('No audio file found.')

    #Uploaded audio file.
    file = request.files['audio']

    if file and valid_filetype(file.filename, filetype):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        subtitles = model.transcribe(path)
        return render_template('index.html', audio=f'../{path}', audio_subtitles=subtitles)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.config.from_pyfile('../config.py')
    app.run(debug=True)