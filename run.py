import eel

from engine.features import *

# Initialize Eel
eel.init('frontend')  # Ensure this points to the folder with your index.html
playAssistantSound()
# Start the application
eel.start('index.html', size=(800, 600))  # Ensure this points to the correct file
