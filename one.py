import sounddevice as sd
import queue
import vosk
import sys
import json

def recognize_audio():
    # Initialize Vosk model and recognizer
    model_path = "/media/kuladeep/d/codes/project-J/vosk-model-en-us-0.22"  # Update this with your model path
    if not model_path:
        print("Please provide a valid Vosk model path.")
        sys.exit(1)

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)  # Sampling rate: 16000 Hz

    # Queue for audio data
    audio_queue = queue.Queue()

    # Callback for streaming audio data to the queue
    def audio_callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(bytes(indata))

    # Start the audio stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Listening... Speak into the microphone.")
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print(f"Recognized Text: {result['text']}")
                return result['text']
            else:
                # Optionally process partial results
                partial = json.loads(recognizer.PartialResult())
                print(f"Partial: {partial['partial']}")

# Run the function
recognized_text = recognize_audio()
print(f"Final Transcription: {recognized_text}")
