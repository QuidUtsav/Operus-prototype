from kokoro_onnx import Kokoro
import sounddevice as sd

kokoro_model = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

def speak(text):
    if not text:
        return
    
    samples, sample_rate = kokoro_model.create(
        text,
        voice="af_heart",
        speed=1.0,
        lang="en-us"
    )
    
    sd.play(samples, sample_rate)
    sd.wait()  
    