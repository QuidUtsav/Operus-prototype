# voice.py
import numpy as np
import sounddevice as sd
from pynput import keyboard

SAMPLE_RATE = 16000  
CHANNELS = 1         

is_recording = False
audio_chunks = []

def audio_callback(indata, frames, time, status):
    if is_recording:
        audio_chunks.append(indata.copy())

def on_press(key):
    global is_recording, audio_chunks
    if key == keyboard.Key.space:
        # clearing previous recording
        audio_chunks = []        
        is_recording = True

def on_release(key):
    global is_recording
    if key == keyboard.Key.space:
        is_recording = False

def record_audio():
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()