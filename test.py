import os
import psutil
import shutil
import pyautogui
from tkinter import *
from tkinter import messagebox
from threading import Thread
import subprocess
import speech_recognition as sr
from datetime import datetime
from gtts import gTTS
import pyjokes,randfacts
import time
import webbrowser as web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests,re
import pywhatkit as kit
import wikipedia

para=''
tele = False
# Globals
recognizer = sr.Recognizer()
assistant_active = True

def textspeech(text):
    tts = gTTS(text=text, lang='en-in', slow=False)
    tts.save("output.wav")
    subprocess.run(['mpv', '--speed=1.2', 'output.wav'])

def start_listening():
    """Start Listening for Commands"""
    global assistant_active
    assistant_active = True
    Thread(target=process_voice_commands).start()

def stop_listening():
    """Stop Listening for Commands"""
    global assistant_active
    assistant_active = False
    log_message("Voice Assistant Stopped.")

def log_message(message):
    """Log Messages in the GUI"""
    log_area.insert(END, message + "\n")
    log_area.see(END)

def wiki(text):
    input = text.replace("browse", "").replace("about", "").strip()
    result = wikipedia.summary(input, sentences=2)
    cleaned_text = result.replace('Hindi','').replace('pronunciation','').strip()
    log_message(cleaned_text)
    textspeech(cleaned_text)

def temperature(text):
    driver = webdriver.Chrome()
    text = text.replace('temperature','').replace('whether','').replace('of','').replace('at','').strip()
    try:
        # Open Wikipedia
        driver.get(f"https://www.google.com/search?q={text}+whether")
        # Find the search input box
        search_box = driver.find_element(By.ID,'wob_tm').text
        driver.quit()
        textspeech(f'temperature at {text} is '+ search_box+ 'degree celsius')
        time.sleep(0.1)
    except Exception as e:
        print(Exception)
        textspeech('not found')
    finally:
        # Close the browser
        driver.quit()

def Telegram():
    textspeech('Opening Telegram...')
    try:
        # Open Telegram Desktop in the background
        subprocess.Popen('telegram-desktop', shell=True)
        textspeech('Telegram is now open.')
    except Exception as e:
        textspeech('Failed to open Telegram.')
        print(f"Error opening Telegram: {e}")


def youTube(text):
    kit.playonyt(text)
    pyautogui.press('k')

def record_audio():
    log_message('listening.......')
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,1.2)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=25)
        text = recognizer.recognize_google(audio).lower()
    return text


def process_voice_commands():
    """Main Voice Processing Loop"""
    global assistant_active
    log_message("Listening for commands...")
    while assistant_active:
        try:
            text = record_audio()
            log_message(f"You said: {text}")
            process_command(text)
        except sr.UnknownValueError:
            log_message("Could not understand the audio.")
        except sr.WaitTimeoutError:
            log_message("Listening timed out.")
        except Exception as e:
            log_message(f"Error: {e}")

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def news():
    apiadress = "https://newsapi.org/v2/everything?q=keyword&apiKey=c2854530a2a44f21a107acddf62832e9"
    json_data = requests.get(apiadress).json()
    for i in range(1,4):
        data = f'Number{i} {json_data['articles'][i]['title']}'
        print({data})
        textspeech(data)


def process_command(text):
    global tele
    """Process Commands"""
    if "exit" in text or "quit" in text:
        stop_listening()
        app.quit()
    elif "browse" in text:
        wiki(text)  
        return
    elif "google" in text:
        textspeech('opening google')
        web.open_new_tab('https://www.google.com/')
        time.sleep(10)
        os.system('pkill chrome')
        return
    elif "search" in text:
        text = text.replace('search', '')
        kit.search(text)
        time.sleep(10)
        os.system('pkill chrome')
        return
    elif "date" in text:
        now = datetime.now()
        formatted_date = now.strftime('%B %d, %Y')
        log_message(f"Date: {formatted_date}")
        textspeech(f"Today's date is {formatted_date}.")
    elif "time" in text:
        now = datetime.now()
        current_time = now.strftime('%I:%M %p')
        log_message(f"Time: {current_time}")
        textspeech(f"The current time is {current_time}.")
    elif "joke" in text:
        joke = pyjokes.get_joke()
        log_message(f"Joke: {joke}")
        textspeech(joke)
    elif "fact" in text:
        fact = randfacts.get_fact()
        log_message(f"Fact: {fact}")
        textspeech(f"Did you know? {fact}")
    elif "play" in text:
         youTube(text)
         return
    elif "news" in text:
        news()
        return
    elif 'whether' in text or 'temperature' in text:
        temperature(text)
        os.system('pkill chrome')
    elif "screenshot" in text:
        take_screenshot()
    elif 'close telegram' in text and tele:
        textspeech('Closing Telegram...')
        pyautogui.hotkey('alt','f4')
        tele = False
        return
    elif 'telegram' in text:
        tele = True
        Telegram()
        return
    elif 'ip' in text:
        ip = find_my_ip()
        print(ip)
        textspeech(ip)
        log_message(ip)
    elif 'terminal' in text and 'open' in text:
        pyautogui.hotkey('ctrl','alt','t')
    elif 'close terminal' in text:
        pyautogui.hotkey('ctrl','shift','q') 
    else:
        log_message("Command not recognized.")

def take_screenshot():
    """Capture and Save Screenshot"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        shutil.move(filename, os.path.join('screenshots', filename))
        log_message(f"Screenshot saved: {filename}")
    except Exception as e:
        log_message(f"Error taking screenshot: {e}")
        textspeech("Failed to take a screenshot.")

# GUI
app = Tk()
app.title("Project -J ")
app.geometry("500x600")

# Header
header_label = Label(app, text="Voice Assistant", font=("Arial", 24, "bold"))
header_label.pack(pady=10)

# Buttons
button_frame = Frame(app)
button_frame.pack(pady=10)

start_button = Button(button_frame, text="Start Listening", font=("Arial", 12), command=start_listening, bg="green", fg="white")
start_button.grid(row=0, column=0, padx=10)

stop_button = Button(button_frame, text="Stop Listening", font=("Arial", 12), command=stop_listening, bg="red", fg="white")
stop_button.grid(row=0, column=1, padx=10)

# Log Area
log_label = Label(app, text="Logs:", font=("Arial", 14))
log_label.pack(pady=5)

log_area = Text(app, wrap=WORD, font=("Arial", 12), height=20)
log_area.pack(padx=10, pady=5, fill=BOTH, expand=True)

# Start GUI
textspeech("Hello, I am your voice assistant. Press Start to begin.")
app.mainloop()
