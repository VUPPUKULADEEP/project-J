import sounddevice as sd
import subprocess
import webbrowser as web
import pyjokes 
import speech_recognition as sr

r = sr.Recognizer()

def record_audio():   
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source,1.2)
        print('Recording audio...')
        print("Please speak something:")
        audio = r.listen(source, timeout=4, phrase_time_limit=10)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            #textspeech('i didnt understand')
            return 'speak again'
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


def textspeech(x,language_code="en-US"):
    # Directly use pico2wave through subprocess
    temp_wav = "audio/temp_speech.wav"  # Temporary file to store speech
    command = f'pico2wave -w {temp_wav} "{x}"'  # Generate speech with pico2wave
    # Run pico2wave command to generate speech
    subprocess.run(command, shell=True , check=True)
    # Play the generated speech using 'aplay'
    subprocess.run(f'aplay {temp_wav}', shell=True)

def open_web(text):
    lower_text = text.lower()
    print(f"Transcription received: '{text}'")
    if "browse" in lower_text:
        web.open("https://www.google.com/search?q=" + text)   
    elif "google" in lower_text:
        textspeech('opening google')
        web.open_new_tab('https://www.google.com/')
    elif "joke" in lower_text and not "don't" in lower_text:
         a_joke = joke()
         print("Joke:", a_joke) 
         textspeech(a_joke)


def joke():
    return pyjokes.get_joke("en","all"); 


textspeech('hello sir iam your voice assistant')

while True:
    text = record_audio()
    open_web(text)
    print("Transcription:", text)

# usr/bin/google-chrome-stable