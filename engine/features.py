import eel
import subprocess

@eel.expose
def playAssistantSound():
     subprocess.run(["ffplay", "-nodisp", "-autoexit", "start_sound.mp3"])