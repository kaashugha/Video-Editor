from google.cloud import speech

speech_client = speech.SpeechClient.from_service_account_json('client_service_key.json')

# LOAD MEDIA FILES
file_name = 'local_audio.mp3'

with open(file_name, 'rb') as f1:
    mp3_data = f1.read()
audio_file = speech.RecognitionAudio(content=mp3_data)

# CONFIGURE MEDIA FILE OUTPUTS
config = speech.RecognitionConfig(
    sample_rate_hertz=44100,
    # encoding="LINEAR16",
    enable_automatic_punctuation=True,
    language_code='en-us',
    enable_word_time_offsets=True
)

# TRANSCRIBING THE RecognitionAudio OBJECTS
# response_standard_mp3 = speech_client.recognize(
#     config=config,
#     audio=audio_file
# )

operation = speech_client.long_running_recognize(config=config, audio=audio_file)

print("Waiting for operation to complete...")
result = operation.result(timeout=90)

for result in result.results:
    alternative = result.alternatives[0]
    print("Transcript: {}".format(alternative.transcript))
    print("Confidence: {}".format(alternative.confidence))

    for word_info in alternative.words:
        word = word_info.word
        start_time = word_info.start_time
        end_time = word_info.end_time

        print(
            f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
        )
