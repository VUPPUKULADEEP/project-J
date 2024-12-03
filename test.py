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
from email.message import EmailMessage
import smtplib
import eel


EMAIL = "vuppukuladeep@gmail.com"
PASSWORD = "ovbu muyi ijnp tvhg"

para=''
tele = False
# Globals
recognizer = sr.Recognizer()
assistant_active = True
recording = True

def textspeech(text):
    tts = gTTS(text=text, lang='en-in', slow=False)
    tts.save("output.wav")
    subprocess.run(['mpv', '--speed=1.2', 'output.wav'])

@eel.expose
def start_listening():
    """Start Listening for Commands"""
    global assistant_active
    assistant_active = True
    Thread(target=process_voice_commands).start()

def stop_listening():
    """Stop Listening for Commands"""
    global assistant_active
    assistant_active = False
    print("Voice Assistant Stopped.")


def wiki(text):
    input = text.replace("browse", "").replace("about", "").strip()
    result = wikipedia.summary(input, sentences=2)
    cleaned_text = result.replace('Hindi','').replace('pronunciation','').strip()
    print(cleaned_text)
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

def record_audio(time,phrase):
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,1.2)
        print('listening.......')
        eel.DisplayMessage('listening.........')
        audio = recognizer.listen(source, timeout=time, phrase_time_limit=phrase)
        eel.DisplayMessage('recognizing.......')
        text = recognizer.recognize_google(audio).lower()
    return text


def process_voice_commands():
    """Main Voice Processing Loop"""
    global assistant_active
    print("Listening for commands...")
    while assistant_active:
        try:
                text = record_audio(5,25)
                print(f"You said: {text}")
                process_command(text)
        except sr.UnknownValueError:
                print("Could not understand the audio.")
        except sr.WaitTimeoutError:
                print("Listening timed out.")
        except Exception as e:
                print(f"Error: {e}")

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]




def record_continuous_audio(max_silence_duration=3, max_total_duration=60):
    """
    Continuously record and process audio, allowing for pauses in speech.
    
    Parameters:
        max_silence_duration (int): Maximum duration of silence (in seconds) before considering input complete.
        max_total_duration (int): Maximum total listening duration (in seconds).
        
    Returns:
        str: Combined recognized text from the audio.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening continuously... Speak now.")
        textspeech("I am listening. Speak now.")
        
        complete_text = ""
        start_time = time.time()
        
        while True:
            try:
                # Listen for a chunk of speech
                audio = recognizer.listen(source, timeout=max_silence_duration, phrase_time_limit=max_silence_duration)
                
                # Recognize the speech in the chunk
                chunk_text = recognizer.recognize_google(audio)
                print(f"Recognized chunk: {chunk_text}")
                complete_text += f" {chunk_text}".strip()
            
            except sr.WaitTimeoutError:
                # Silence detected; check if maximum silence duration is reached
                if time.time() - start_time >= max_total_duration:
                    print("Maximum listening duration reached.")
                    break
                else:
                    print("Pause detected, waiting for further input...")
                    textspeech("You paused, but I am still listening.")
            
            except sr.UnknownValueError:
                print("Could not understand the audio. Waiting for more input...")
            
            except Exception as e:
                print(f"Error during speech recognition: {e}")
                break
            
            # Break the loop if total duration exceeds the maximum limit
            if time.time() - start_time >= max_total_duration:
                print("Reached maximum allowed duration for listening.")
                break

        print(f"Complete recognized text: {complete_text}")
        textspeech("I have captured your speech.")
        return complete_text


def get_subject_and_message():
    """Fetch subject and message via speech."""
    try:
        # Get Subject
        textspeech("Please say the subject of your email.")
        print("Listening for the subject...")
        eel.DisplayMessage('now say the subject')
        subject = record_continuous_audio(max_silence_duration=3, max_total_duration=20)  # Adjust durations as needed
        print(f"Subject received: {subject}")
        eel.DisplayMessage(f"Subject received: {subject}")
        
        # Get Message
        textspeech("Now, please say the message.")
        print("Listening for the message...")
        eel.DisplayMessage('listening for message')
        message = record_continuous_audio(max_silence_duration=4, max_total_duration=30)  # Adjust durations as needed
        print(f"Message received: {message}")
        eel.DisplayMessage(f"Message received: {message}")
        
        return subject, message
    except Exception as e:
        print(f"Error capturing subject and message: {e}")
        textspeech("An error occurred while capturing the subject and message.")
        return None, None



def send_email():
    eel.DisplayMessage('send')
        # Fetch input for receiver email
    eel.i()()


@eel.expose
def sending(receiver):
    try:
        # Fetch subject and message via voice
        subject, message = get_subject_and_message()

        if not subject or not message:
            print("Subject or message not provided. Email sending cancelled.")
            textspeech("Subject or message not provided. Email sending cancelled.")
            return

        # Compose and send the email
        text = f"Subject: {subject}\n\n{message}"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, receiver, text)
        server.quit()

        print(f"Email sent to {receiver}.")
        textspeech("Email has been sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        process_command()




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
    lower_text = text.lower()
    print(f"Transcription received: '{text}'")

    greetings = ["hi", "hello", "hey", "howdy", "hola"]
    farewells = ["bye", "goodbye", "see you", "take care"]
    
    # Time-specific greetings
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        time_greeting = "Good morning!"
    elif 12 <= current_hour < 18:
        time_greeting = "Good afternoon!"
    else:
        time_greeting = "Good evening!"


    if "exit" in text or "quit" in text or "bye" in text:
        textspeech("Goodbye! Have a great day!")
        stop_listening()
    elif any(greet in lower_text for greet in greetings):
        textspeech(f"{time_greeting} How can I assist you today?")

    elif any(farewell in lower_text for farewell in farewells):
        textspeech("Goodbye! Have a great day!")

    elif "how are you" in lower_text:
        textspeech("I'm just a bot, but I'm doing great! How about you?")

    elif "name" in lower_text:
        textspeech("My name is J.A.R.V.I.S, your friendly assistant.")
    
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
        print(f"Date: {formatted_date}")
        textspeech(f"Today's date is {formatted_date}.")
    elif "time" in text:
        now = datetime.now()
        current_time = now.strftime('%I:%M %p')
        print(f"Time: {current_time}")
        textspeech(f"The current time is {current_time}.")
    elif "joke" in text:
        joke = pyjokes.get_joke()
        print(f"Joke: {joke}")
        textspeech(joke)
    elif "fact" in text:
        fact = randfacts.get_fact()
        print(f"Fact: {fact}")
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
        print(ip)
    elif 'terminal' in text and 'open' in text:
        pyautogui.hotkey('ctrl','alt','t')
    elif 'close terminal' in text:
        pyautogui.hotkey('ctrl','shift','q') 
    elif 'send email' in text:
        send_email()
    elif 'cancel email' in text:
        print('cancel')
    elif 'message' in text:
        kit.sendwhatmsg('+919032340532','hi',17,38)
    else:
        print("Command not recognized.")

def take_screenshot():
    """Capture and Save Screenshot"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        shutil.move(filename, os.path.join('screenshots', filename))
        print(f"Screenshot saved: {filename}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        textspeech("Failed to take a screenshot.")


