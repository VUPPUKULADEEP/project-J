import re
import subprocess
import webbrowser as web
import pyjokes 
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import randfacts

r = sr.Recognizer()
para = ''


def textspeech(x,language_code="en-US"):
    # Directly use pico2wave through subprocess
    temp_wav = "audio/temp_speech.wav"  # Temporary file to store speech
    command = f'pico2wave -w {temp_wav} "{x}"'  # Generate speech with pico2wave
    # Run pico2wave command to generate speech
    subprocess.run(command, shell=True , check=True)
    # Play the generated speech using 'aplay'
    subprocess.run(f'aplay {temp_wav}', shell=True)


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


def youTube(text):
    input = text.replace("play", "").replace("youtube", "").strip()
    driver = webdriver.Chrome()
    # Open YouTube, search for a video, and play the first result
    driver.get("https://www.youtube.com/results?search_query="+ input)
    video = driver.find_element(By.ID,'title-wrapper')
    video.click()
    time .sleep(120)


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
            print("Google Speech Recognition could not understand audio")
            #textspeech('i didnt understand')
            return 'speak again'
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


def open_web(text):
    lower_text = text.lower()
    print(f"Transcription received: '{text}'")
    if "browse" in lower_text:
        wikipedia(text)  
    elif "google" in lower_text:
        textspeech('opening google')
        web.open_new_tab('https://www.google.com/')
    elif "joke" in lower_text and not "don't" in lower_text:
         a_joke = joke()
         print("Joke:", a_joke) 
         textspeech(a_joke)
    elif "play" in lower_text:
         youTube(text)
    elif "news" in lower_text:
        news()
    elif "welcome back daddy's home" in lower_text:
        textspeech('welocome back sir all set')
    elif "fact" or "facts" in lower_text:
        x = random_facts()
        print(x)
        textspeech('did you know that  '+  x)


def joke():
    return pyjokes.get_joke("en","all"); 


def news():
    apiadress = "https://newsapi.org/v2/everything?q=keyword&apiKey=c2854530a2a44f21a107acddf62832e9"
    json_data = requests.get(apiadress).json()
    for i in range(1,4):
        data = f'Number{i} {json_data['articles'][i]['title']}'
        print({data})
        textspeech(data)


def temp():
    url = 'http://api.weatherapi.com/v1/current.json?key=ece7dca8c7904b3e8e0131221242911&q=Srikakulam&aqi=no'
    json_data = requests.get(url).json()
    print(json_data)
    print(json_data['current']['wind_mph'])
    print(json_data['current']['temp_c'])
    print(json_data['current']['humidity'])
    print(json_data['current']['condition']['text'])

    textspeech(f'At Srikakulam,  wind speed is  {json_data['current']['wind_mph']} meters per hour, temperature is {json_data['current']['temp_c']}, humidity is {json_data['current']['humidity']} and present condition {json_data['current']['condition']['text']}')


textspeech('hello sir iam your voice assistant')


while True:
    text = record_audio()
    textspeech(text)
    open_web(text)
    print("Transcription:", text)

temp()

