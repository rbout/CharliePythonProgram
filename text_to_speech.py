from google.cloud import texttospeech

# Synthesizes speech from the input string of text or ssml
def gtts_custom(watson_res, file_name):
    # Instantiate a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=watson_res)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US', name='en-US-Wavenet-I'
    )

    # Set the audio file type to be returned as MP3
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary
    with open(file_name, 'wb') as out:
        # Write the response to the output file
        out.write(response.audio_content)