# voice.py
import numpy as np
import sounddevice as sd
from pynput import keyboard
from faster_whisper import WhisperModel

whisper_model = WhisperModel("small", device="cpu", compute_type="int8")

SAMPLE_RATE = 44100  
CHANNELS = 1         

is_recording = False
audio_chunks = []

def audio_callback(indata, frames, time, status):
    if is_recording:
        audio_chunks.append(indata.copy())

def on_press(key):
    global is_recording, audio_chunks
    print("on-press activate")
    if key == keyboard.Key.space:
        # clearing previous recording
        audio_chunks = []        
        is_recording = True

def on_release(key):
    print("key released")
    global is_recording
    if key == keyboard.Key.space:
        is_recording = False
        return False

def record_audio():
    global is_recording, audio_chunks
    audio_chunks = []
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback, device='default'):
        input("Press Enter to start recording...")
        is_recording = True
        input("Press Enter to stop recording...")
        is_recording = False


def transcribe(audio_chunks):
    if not audio_chunks:
        return ""
    
    audio = np.concatenate(audio_chunks, axis=0)  
    audio = audio.squeeze()                       
    audio = audio.astype(np.float32)               
    
    import scipy.signal
    audio = scipy.signal.resample(audio, int(len(audio) * 16000 / 44100))

    segments, _ = whisper_model.transcribe(audio, language="en")
    text = " ".join([s.text for s in segments])
    return text.strip()

def record_audio_and_transcribe():
    record_audio()
    return transcribe(audio_chunks=audio_chunks)