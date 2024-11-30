import os
import re
import subprocess
from gtts import gTTS
import webbrowser as web
import pyjokes 
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import randfacts
from datetime import datetime
import pyautogui
import mouseinfo,shutil
import keyboard

r = sr.Recognizer()
now= datetime.now()
para = ''


def textspeech(text):
    tts = gTTS(text=text, lang='en-in', slow=False)
    tts.save("output.wav")
    subprocess.run(['mpv', '--speed=1.2', 'output.wav'])

def wikipedia(text):
    global para
    input = text.replace("browse", "").replace("about", "").strip()
    # Initialize the WebDriver (Chrome in this case)
    driver = webdriver.Chrome()
    try:
        # Open Wikipedia
        driver.get("https://www.wikipedia.org")
        # Find the search input box
        search_box = driver.find_element(By.ID,'searchInput')
        search_button=driver.find_element(By.TAG_NAME,'button')
        search_box.send_keys(input)
        search_button.click()
        para = driver.find_element(By.XPATH,'//*[@id="mw-content-text"]/div[1]/p[2]').text 
        cleaned_text=re.sub(r'[^a-zA-Z0-9\s]', '', para)
        print(cleaned_text)
        time.sleep(5)
        textspeech(cleaned_text)
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
    input = text.replace("play", "").replace("youtube", "").strip()
    driver = webdriver.Chrome()
    # Open YouTube, search for a video, and play the first result
    driver.get("https://www.youtube.com/results?search_query="+ input)
    video = driver.find_elements(By.ID,'title-wrapper')
    video[1].click()
    try:
        # Wait for the "Skip Ads" button to be clickable
        skip_button = WebDriverWait(driver, 12).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Skip Ads')]"))
        )
        skip_button.click()  # Click the skip button
        print("Ad skipped!")
    except Exception as e:
        print("No ad to skip or an error occurred:", e)
    time .sleep(120)
    driver.quit()

def random_facts():
    return randfacts.get_fact()


def record_audio():   
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source,1.2)
        print('Recording audio...')
        print("Please speak something:")
        audio = r.listen(source, timeout=4, phrase_time_limit=12)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            return 'speak again'
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


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

def take_screenshot():
    """Capture and Save a Screenshot"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    shutil.move(filename, os.path.join('screenshots', filename))
    textspeech(f"Screenshot saved as {filename}")
    print(f"Screenshot saved as {filename}")


def open_web(text):
    lower_text = text.lower()
    print(f"Transcription received: '{text}'")
    if "browse" in lower_text:
        wikipedia(text)  
        return
    elif "google" in lower_text:
        textspeech('opening google')
        web.open_new_tab('https://www.google.com/')
        time.sleep(10)
        os.system('pkill chrome')
        return
    elif "search" in lower_text:
        text = text.replace('search', '')
        web.open_new_tab(f'https://www.google.com/search?query={text}')
        time.sleep(10)
        os.system('pkill chrome')
        return
    elif "joke" in lower_text and not "don't" in lower_text:
         a_joke = joke()
         print("Joke:", a_joke) 
         textspeech(a_joke)
         return
    elif "play" in lower_text:
         youTube(text)
         return
    elif "news" in lower_text:
        news()
        return
    elif 'whether' in lower_text or 'temperature' in lower_text:
        temperature(text)
        os.system('pkill chrome')
    elif "fact" in lower_text or "facts" in lower_text:
        x = random_facts()
        print(x)
        textspeech('did you know that  '+  x)
        return
    elif 'date' in lower_text:
        now = datetime.now()
        formatted_date = now.strftime('%B %d, %Y')
        print(formatted_date)
        textspeech(formatted_date)
        return
    elif 'time' in lower_text:
        now = datetime.now() 
        tim =now.strftime('%I:%M%p')
        print(tim)
        textspeech(tim)
        return
    elif "take" in lower_text and "picture" in lower_text:
        take_screenshot()
    elif 'close telegram' in lower_text:
        textspeech('Closing Telegram...')
         # Simulate pressing Alt + F4
        keyboard.press_and_release('alt+f4')
    elif 'telegram' in lower_text:
        Telegram()
    else:
        return
 


def joke():
    return pyjokes.get_joke("en","all"); 


def news():
    apiadress = "https://newsapi.org/v2/everything?q=keyword&apiKey=c2854530a2a44f21a107acddf62832e9"
    json_data = requests.get(apiadress).json()
    for i in range(1,4):
        data = f'Number{i} {json_data['articles'][i]['title']}'
        print({data})
        textspeech(data)


textspeech('hello sir i am your voice assistant')
 

while True:
    text = record_audio()
    if 'exit' in text:
        break
    if text is not 'speak again':
        open_web(text)
    print("Transcription:", text)




