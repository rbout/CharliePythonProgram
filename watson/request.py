""" Creates an HTTP POST request given to our web server
    in order to send the given text as an intent to IBM
    Watson. Watson then responds with text output. The 
    text output is passed as an argument and synthesized
    by the Google Cloud TTS API in order to be returned
    as an audio output file and played back.
"""
try:
    from playsound import playsound
    from . import text_to_speech
    import requests
except Exception as e:
    print('[Request] Import Error: {}'.format(e))

# Creates a POST request to our Node.js server with
# the given intent text
def speech_to_text_request(intent, filename):
    try:
        res = requests.post('https://charlierobotserver.herokuapp.com/talk',
                            json={'text': intent}).text
        print('Charlie Response: {}'.format(res))
        text_to_speech.gtts_custom(res, filename)
        playsound(filename)
    except requests.exceptions.TooManyRedirects:
        print('[Request] Request Error: Bad URL')
    except requests.exceptions.RequestException as e:
        raise SystemExit('[Request] {}'.format(e))
