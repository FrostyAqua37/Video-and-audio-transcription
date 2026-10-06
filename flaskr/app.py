from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from transcribe import MediaTranscriber
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        video_transcriber = MediaTranscriber(path, type='video')
        video_transcriber.transcribe()
        subtitles = video_transcriber.format_subtitles()
        
        return render_template('index.html', subtitles=subtitles)
    
    return redirect(url_for('index'))


@app.route('/display/<filename>')
def display_video(filename:str):
    return redirect(url_for('static', filename='uploads/' + filename)) 

if __name__ == "__main__":
    app.config.from_pyfile('../config.py')
    app.run(debug=True)