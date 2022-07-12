import moviepy.editor as mp
import os
from flask import Flask, render_template, request, flash
from google.cloud import speech

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  'client_service_key.json'
# speech_client = speech.SpeechClient

# # LOAD MEDIA FILES
# media_file_name_m4a = 'local_audio.m4a'

# with open(media_file_name_m4a, 'rb') as f1:
#     byte_data_mp3 = f1.read()
# audio_m4a = speech.RecognitionAudio(content=byte_data_mp3)

# # CONFIGURE MEDIA FILE OUTPUTS
# config_mp3 = speech.RecognitionConfig(
#     sample_rate_hertz=48000,
#     enable_automatic_punctuation=True,
#     language_code='en-us'
# )




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

    for file in request.files.getlist('file'):
        print(file)
        video_filename = file.filename
        destination ='/'.join([target_video, video_filename])
        print(destination)
        file.save(destination)
        video_file = mp.VideoFileClip(target_video + video_filename)
        audio_filename = target_audio + os.path.splitext(video_filename)[0] + '.mp3'
        video_file.audio.write_audiofile(audio_filename)
        
    

    return render_template("cuttingroom.html")

@app.route("/transcribe", methods=['POST'])
def transcribe():
    pass