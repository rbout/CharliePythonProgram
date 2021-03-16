from gtts import gTTS
from playsound import playsound
import requests
import sys

filename = 'output.mp3'

if len(sys.argv) == 2:
    res = requests.post("https://charlierobotserver.herokuapp.com/talk", json={"text": sys.argv[1]}).text
    tts = gTTS(res, lang='en')
    tts.save(filename)
    playsound(filename)
else:
    print("Need question in the command line for the time being")
