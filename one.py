import sounddevice as sd
from scipy.io.wavfile import write
import whisper


# installation command pip install openai-whisper
# Parameters for recording
sample_rate = 16000  # Sampling frequency
duration = 10  # Duration of recording in seconds
output_file = "recorded_audio.wav"  # Output file name

# Step 1: Record Audio
print("Recording... Speak now!")
audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()  # Wait until the recording is finished
write(output_file, sample_rate, audio_data)  # Save as a WAV file
print(f"Recording complete. Audio saved as {output_file}.")

# Step 2: Load Whisper Model
print("Loading Whisper model...")
model = whisper.load_model("tiny", device="cpu")  # Use "cpu" explicitly for CPU processing

# Step 3: Transcribe the Recorded Audio
print("Transcribing audio...")
result = model.transcribe(output_file,language='en')

# Step 4: Output the Transcription
print("Transcription:")
print(result["text"])
