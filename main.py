import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import subprocess
from faster_whisper import WhisperModel
import webbrowser as web

# Initialize the Whisper model
model = WhisperModel("tiny.en", device="cpu")  # Change "small" to another model if needed

# Audio recording settings
sample_rate = 16000  # Whisper models work well with 16kHz audio
duration = 5  # Duration of recording in seconds

def record_audio():
    print("Recording audio...")
    audio = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    audio = np.squeeze(audio)  # Remove single-dimensional entries from the array
    sd.stop()
    # print(audio)
    return audio

def save_audio_as_wav(audio, filename="recording.wav"):
    # Convert float32 audio data to int16 for WAV file compatibility
    scaled_audio = np.int16(audio * 32767)
    # print(scaled_audio)
    wav.write(filename, sample_rate, scaled_audio)

def transcribe_audio(filename="recording.wav", language="en"):
    segments, info = model.transcribe(filename)
    # print(f"Detected language: {info.language} with probability {info.language_probability:.2f}")
    
    # Print each segment
    transcription = ""
    for segment in segments:
        transcription += segment.text + " "
    return transcription

def textspeech(x,language_code="it-US"):
    # Directly use pico2wave through subprocess
    temp_wav = "audio/temp_speech.wav"  # Temporary file to store speech
    command = f'pico2wave -w {temp_wav} "{x}"'  # Generate speech with pico2wave
    # Run pico2wave command to generate speech
    subprocess.run(command, shell=True)
    # Play the generated speech using 'aplay'
    subprocess.run(f'aplay {temp_wav}', shell=True)

def open_web(text):
    if "google" in text.lower():
        textspeech('opening google')
        web.open_new('https://www.google.com/')

# Record and transcribe
audio_data = record_audio()
save_audio_as_wav(audio_data) #   Save the recording to a file
text = transcribe_audio()
textspeech(text)  # Transcribe the recorded audio file
open_web(text)
print("Transcription:", text)