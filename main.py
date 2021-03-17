from playsound import playsound
from text_to_speech import gtts_custom
import requests
import speech_recognition as sr
import sys

filename = 'output.mp3'
r = sr.Recognizer()
intent = ''

with sr.Microphone() as source:
    print('Ask Charlie a question:')
    audio = r.listen(source)

try:
    intent = r.recognize_google(audio)
    print('Your Intent: {}'.format(intent))
except:
    print('Sorry, could not understand your intent...')
    quit()

try:
    res = requests.post('https://charlierobotserver.herokuapp.com/talk', json={'text': intent}).text
    print('Charlie Response: {}'.format(res))
    gtts_custom(res, filename)
    playsound(filename)
except requests.exceptions.TooManyRedirects:
    print('[Text-To-Speech] Request Error: Bad URL')
except requests.exceptions.RequestException as e:
    raise SystemExit('[Text-To-Speech] {}'.format(e))
