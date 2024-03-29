from flask import Flask, render_template, request
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)

# Create a recognizer object
recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        return "No audio file uploaded"
    
    file = request.files['audio_file']
    
    if file.filename == '':
        return "No selected file"
    
    try:
        # Convert MP3 audio to WAV
        audio = AudioSegment.from_mp3(file)
        audio.export("temp.wav", format="wav")
        
        # Use the recognizer to open the temporary WAV file
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)

            # Recognize the speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
