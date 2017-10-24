import argparse
import io
import os


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    #temp_file_name = "./export.wav"

    #os.remove(temp_file_name)

    #from pydub import AudioSegment
    #sound = AudioSegment.from_mp3(speech_file)
    #"-acodec", "pcm_s16le" ,
    #sound.export(temp_file_name, format="flac", parameters=["-ac", "1","-ar", "16000" ])

    #os.system("ffmpeg -i #{speech_file} #{temp_file_name}")

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Print the first alternative of all the consecutive results.

    print(response)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

transcribe_file('/home/kruszynka/Pobrane/Source/mastercoder/fakap-team/plikiaudio/rozmowa1_ENG/scen1tel2.flac')
