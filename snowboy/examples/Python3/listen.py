""" Implements Snowboy Hotword Detection allowing the
    machine to listen out for custom wake words.
    Snowboy no longer receives support from KITT.AI

    Instead, we refer to this GitHub Repo:
    https://github.com/seasalt-ai/snowboy
"""
import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
sys.path.append('../../..')
from watson.request import speech_to_text_request

interrupted = False # Used to handle interrupt command (Ctrl+C)
output_path = 'output.mp3'

# Record audio for intent after hearing 'Hey, Charlie!'
def audio_record_callback(file_name):
    r = sr.Recognizer()
    intent = ''

    with sr.AudioFile(file_name) as source:
        audio = r.record(source)  # Read the audio file
    try:
        intent = r.recognize_google(audio)
        print('Your Intent: {}'.format(intent))
        os.remove(file_name)
        # Exit if the intent is a goodbye
        if intent == 'goodbye':
            snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
            quit()
        # Otherwise, send the request
        speech_to_text_request(intent, output_path)
    except sr.UnknownValueError:
        os.remove(file_name)
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        os.remove(file_name)
        print('Could not request results from Google Speech Recognition service; {}'.format(e))
    # Tried calling 'os.remove(file_name)' once at the bottom here but did not seem to work

# Callback for 'Hey, Charlie!'
def detected_greeting():
  snowboydecoder.play_audio_file()
  print('Ask Charlie a question:')

def interrupt_callback():
    global interrupted
    return interrupted

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

if len(sys.argv) == 1:
    print('Error: You must specify a model name')
    print('Usage: python3 listen.py hey_charlie.pmdl')
    sys.exit(-1)

model = sys.argv[1] # The model files passed in as arguments

# Capture SIGINT Signal (i.e. Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Charlie Listening... Press Ctrl+C to exit')

# Main Loop
detector.start(detected_callback=detected_greeting,
               audio_recorder_callback=audio_record_callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
