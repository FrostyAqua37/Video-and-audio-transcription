from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from resources.transcribe import Transcribe
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from shortuuid import uuid
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config.from_pyfile('../config.py', silent=True)

model = Transcribe()

ALLOWED_EXTENSIONS = {
    #Dictionaries with filetypes that are accepted.
    "video": {"mp4", "avi", "mov", "wmv", "ogg", "webm", "mkv", "flv"},
    "audio": {"mp3", "wav", "flac", "wma", "aac", "aiff", "ogg", "midi"},
}

def valid_filetype(filename:str, filetype:str) -> bool:
    #Checks if file is an allowed extension.
    if filetype not in ALLOWED_EXTENSIONS or not filename:
        return False

    #Finds extension from filename and checks it
    suffix = Path(filename).suffix.lower().lstrip('.')
    return suffix in ALLOWED_EXTENSIONS[filetype]

def process_upload(filetype:str):
    #Validate, save and transcribe uploaded media file.
    media_file = request.files.get(filetype)
    
    if media_file is None or not media_file.filename:
        flash(f'No {filetype} file selected.')
        return redirect(url_for('index'))

    if not valid_filetype(media_file.filename, filetype):
        flash(f'Unsupported {filetype} file format.')
        return redirect(url_for('index'))

    secure_file = secure_filename(media_file.filename)

    if not secure_file:
        flash('Invalid filename.')
        return redirect(url_for('index'))

    upload_dir = Path(app.config['UPLOAD_FOLDER'])
    upload_dir.mkdir(parents=True, exist_ok=True)    #Makes a new directory within upload folder path

    filename = f'{uuid()[:10]}_{secure_file}'   #Generates random string of characters to prevent different uploads to overwrite each other.
    file_path = upload_dir / filename

    try:
        #Saves and transcribes media file.
        media_file.save(file_path)
        subtitles = model.transcribe(str(file_path))
        file_name = media_file.filename.lower().split('.')[0]   #Filename without extension

        #Exports video file transcriptions as text file and pdf.
        text_file = save_as_text(file_name, 'txt', subtitles)
        #save_as_pdf(file_name, subtitles)

    except Exception:
        app.logger.exception(f'Failed to process {filetype} file.')
        
        #Removes saved media file if the process failed
        file_path.unlink(missing_ok=True)
        flash(f'Could not process the {filetype} file.')
        return redirect(url_for('index'))
    
    #Returns home page and unpacks filepath and transcribed text.
    return render_template(
        'index.html',
        **{
            filetype: url_for('static', filename=f'uploads/{filename}'),
            'text_file': text_file,
            #'pdf': upload_dir / f'{file_name}.pdf',
        },
    )

@app.route('/', methods=['GET'])
def index():
    #Returns the home page.
    return render_template('index.html')

@app.route('/video', methods=['POST'])
def video():
    return process_upload('video')

@app.route('/audio', methods=['POST'])
def audio():
    return process_upload('audio')

def save_as_text(filename:str, filetype:str, subtitles:list):
    path = Path(app.config['UPLOAD_FOLDER'])
    text_file = open(f'{path}/{filename}.{filetype}', 'w')

    for subtitle in subtitles:
        text_file.write(f'[{subtitle["timestamp"]}] {subtitle["text"]}')
        text_file.write('\n')

    text_file.close()
    return text_file.name

def save_as_pdf(filename:str, subtitles:list):
    #Saving subtitles in a pdf document
    save_dir = f'{app.config["UPLOAD_FOLDER"]}/{filename}.pdf'
    subtitle = '*This transcription was done through OpenAI Whisper.'  

    pdf = canvas.Canvas(save_dir)  
    pdf.setTitle(filename)
    pdf.setFont('Courier', 20)

    #Sets title and subtitle at x, y position
    pdf.drawCentredString(300, 770, filename.capitalize())  
    pdf.setFont('Courier', 18)
    pdf.drawCentredString(290, 720, subtitle)

    pdf.line(30, 690, 550, 690)
    text = pdf.beginText(40, 650)
    pdf.setFont('Courier', 14)

    for subtitle in subtitles:
        line = f'[{subtitle["timestamp"]}] {subtitle["text"]}'
        text.textLine(line)

    pdf.drawText(text)
    pdf.save()

if __name__ == "__main__":
    app.run(debug=True)