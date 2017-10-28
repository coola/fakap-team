import io
import os
import sys
import time
import datetime

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


from pydub import AudioSegment

def transcribe_file(args):

    if len(sys.argv) != 4 or not args[1] or not args[2] or not args[3]:
        print "Usage: python transcribeFile.py [speech_folder_path] [keywords_file_path] [language_code en-US or pl-PL]"
        print "Example: python transcribeFile.py /home/kruszynka/Pobrane/Source/mastercoder/fakap-team/plikiaudio/rozmowa1_ENG/ /home/kruszynka/Pobrane/Source/mastercoder/fakap-team/plikiaudio/keywords_ENG.txt en_US"
        return


    speech_folder = args[1]
    keywords_file = args[2]
    language_code = args[3]

    directory = 'temp'

    if not os.path.exists(directory):
        os.makedirs(directory)  

    current_temp_directory = directory + "/" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
    os.makedirs(current_temp_directory) 

    client = speech.SpeechClient()


    print("Converting mp3 files to wav files")
    for filename in os.listdir(speech_folder):
        if filename.endswith(".mp3"): 
            path = os.path.join(speech_folder, filename)
            sound = AudioSegment.from_mp3(path)
            flac_path = os.path.join(current_temp_directory, filename + '.flac')
            sound.export(flac_path, format="flac", parameters=["-ac", "1","-ar", "16000" ])
            print("converting" + path)
            print("         to")
            print("           "+ flac_path)
            continue
        else:
            continue

    for filename in os.listdir(current_temp_directory):
        if filename.endswith(".flac"):            
            flac_path = os.path.join(current_temp_directory, filename)

            splittedFileReport = flac_path + "_splitted.txt"

            print(flac_path)
            print(splittedFileReport)

            print(os.system('ffmpeg -i "'+flac_path+'" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> ' + splittedFileReport))

            print("recognizing file: " + flac_path)
            with io.open(flac_path, 'rb') as audio_file:
                content = audio_file.read()

            audio = types.RecognitionAudio(content=content)
            config = types.RecognitionConfig(
            encoding= enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code=language_code)

            response = client.recognize(config, audio)
            for result in response.results:
                print('Transcript of {}: {}'.format(filename, result.alternatives[0].transcript))
            continue
        else:
            continue
    
    
    # Print the first alternative of all the consecutive results.

    
    print(response)


#'/home/kruszynka/Pobrane/Source/mastercoder/fakap-team/plikiaudio/rozmowa1_ENG/'
transcribe_file(sys.argv)
