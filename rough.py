from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.space:
        print("recording started")

def on_release(key):
    if key == keyboard.Key.space:
        print("recording stopped")
        return False  # stops the listener

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()