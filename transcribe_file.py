import argparse
import io

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    from pydub import AudioSegment
    sound = AudioSegment.from_mp3(speech_file)
    sound.export("./", format="wav")

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Print the first alternative of all the consecutive results.

    print(response)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

transcribe_file('/home/kruszynka/Pobrane/plikiaudio/rozmowa1_ENG/scen1tel1.mp3')