import moviepy.editor as mp
import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/upload", methods=['POST'])
def upload():
    target_video = os.path.join(APP_ROOT, 'videos/')
    target_audio = os.path.join(APP_ROOT, 'audio/')

    if not os.path.isdir(target_video):
        os.mkdir(target_video)
    elif not os.path.isdir(target_audio):
        os.mkdir(target_audio)

    if not request.files.get('file', None):
        flash('sup', 'error')
    else:
        for file in request.files.getlist('file'):
            print(file)
            video_filename = file.filename
            destination ='/'.join([target_video, video_filename])
            print(destination)
            file.save(destination)
            video_file = mp.VideoFileClip(target_video + video_filename)
            audio_filename = target_audio + os.path.splitext(video_filename)[0] + '.mp3'
            video_file.audio.write_audiofile(audio_filename)
    
        
    

    return render_template("success.html")