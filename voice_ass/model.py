import queue
import sounddevice as sd
import vosk
import sys
import json
from datetime import datetime
import random
from difflib import get_close_matches
import pyttsx3 
import soundfile as sf

# === Configuration ===
WAKE_WORDS = ["hey nova", "nova", "wakeup nova"]
STOP_WORD = "goodbye"
MODEL_PATH = r"D:\programing\pythan\voice_ass\vosk-model-en-in-0.5"

# === Track device states ===
device_states = {
    "light": False,
    "door": False,
    "fan": False,
    "bulb": False,
    "all_devices": False
}

def turn_device(device, turn_on):
    current_state = device_states[device]
    if turn_on and current_state:
        return f"The {device} is already on."
    elif not turn_on and not current_state:
        return f"The {device} is already off."
    else:
        device_states[device] = turn_on
        action = "on" if turn_on else "off"
        return f"Turning {action} the {device}."

def turn_all(turn_on):
    for key in device_states:
        device_states[key] = turn_on
    action = "on" if turn_on else "off"
    return f"Turning {action} all electric devices."

COMMANDS = {
    "switch on the light": lambda: turn_device("light", True),
    "switch off the light": lambda: turn_device("light", False),
    "open the door": lambda: turn_device("door", True),
    "close the door": lambda: turn_device("door", False),
    "turn on the fan": lambda: turn_device("fan", True),
    "turn off the fan": lambda: turn_device("fan", False),
    "switch off all electric devices": lambda: turn_all(False),
    "switch on all electric devices": lambda: turn_all(True),
    "what's the time": lambda: f"The time is {datetime.now().strftime('%H:%M:%S')}",
    "tell me the time": lambda: f"The time is {datetime.now().strftime('%H:%M:%S')}",
    "you work very hard": lambda: random.choice([
        "Thank you! I try my best.",
        "That's kind of you to say!",
        "Appreciate it a lot!"
    ]),
    "you are very smart": lambda: random.choice([
        "You're too kind!",
        "Smart thanks to you!",
        "Thanks, that means a lot."
    ]),
    "you are beautiful": lambda: "You're sweet to say that!",
    "i love you": lambda: "Aww, I love helping you too!"
}

# === Initialize Components ===
q = queue.Queue()
VOCABULARY = list(COMMANDS.keys()) + [STOP_WORD]
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000, json.dumps(VOCABULARY))

# === Detect and List Devices ===
print("\n=== All Available Audio Devices ===")
devices = sd.query_devices()
for i, dev in enumerate(devices):
    print(f"{i}: {dev['name']} - Input: {dev['max_input_channels']}, Output: {dev['max_output_channels']}")

# === SET YOUR DEVICE INDEXES HERE ===
INPUT_DEVICE_INDEX = None 
OUTPUT_DEVICE_INDEX = None 

# === Set sounddevice input/output ===
sd.default.device = (INPUT_DEVICE_INDEX, OUTPUT_DEVICE_INDEX)

# === Speak text using pyttsx3 ===
engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 175) 
    engine.setProperty('volume', 0.9) 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[2].id)  
    print(f"[Assistant]: {text}")
    engine.say(text) 
    engine.runAndWait() 

# === Microphone callback ===
def callback(indata, frames, time, status):
    if status:
        print("Mic Status:", status, file=sys.stderr)
    q.put(bytes(indata))

# === Handle voice command ===
def handle_command(command):
    command = command.lower()
    matches = get_close_matches(command, COMMANDS.keys(), n=1, cutoff=0.6)
    if matches:
        match = matches[0]
        response = COMMANDS[match]
        if callable(response):
            speak(response())
        else:
            speak(response)
        print(f"[Matched]: {match}")
    else:
        speak("Sorry, I didn't understand that.")
        print("[No Match]")

# === Main Assistant Loop ===
def run_assistant():
    print(f"\nListening... (say '{' or '.join(WAKE_WORDS)}' to activate)")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback, device=INPUT_DEVICE_INDEX):
        triggered = False
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                print(f"[Heard]: {text}")

                if not triggered:
                    wake_matches = get_close_matches(text, WAKE_WORDS, n=1, cutoff=0.6)
                    if wake_matches:
                        speak("Yes, BOSS! What can I do for you?")
                        triggered = True
                else:
                    if STOP_WORD in text:
                        speak("Goodbye, BOSS. Going silent now.")
                        triggered = False
                    elif text:
                        handle_command(text)
            else:
                # Get the partial recognition result (lowercase for consistency)
                partial = json.loads(recognizer.PartialResult()).get("partial", "").lower()

                if not triggered:
                    # Check if any of the wake words (exact or fuzzy match) are present in the partial text
                    wake_matches = get_close_matches(partial, WAKE_WORDS, n=1, cutoff=0.6)
                    if wake_matches or any(wake_word in partial for wake_word in WAKE_WORDS):
                        speak("Yes, BOSS! What can I do for you?")
                        triggered = True
                elif partial:
                    print(f"[Partial]: {partial}", end='\r')

# === Start Assistant ===
try:
    run_assistant()
except KeyboardInterrupt:
    print("\n[EXIT] Voice assistant stopped.")
