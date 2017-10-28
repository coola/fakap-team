import io
import os
import sys
import time
import datetime
import pprint
import re
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

    current_temp_directory = directory + "/" + str(time.time())
    
    os.makedirs(current_temp_directory) 

    client = speech.SpeechClient()

    recognition_results = []

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

            silenceRecoginitionCommand = 'ffmpeg -i "'+ flac_path +'" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> ' + splittedFileReport

            print silenceRecoginitionCommand

            os.system(silenceRecoginitionCommand)

            voice_start = 0
            voice_duration = 0

            splitted_file_index = 0
            silence_detect_index = 0 
            with open(splittedFileReport) as fileReport:
                for i, line in enumerate(fileReport):                     
                                                      
                    if line.startswith('[silencedetect'):
                                               
                        data = line.split()

                        print '* silence_detect_index ' + str(silence_detect_index) 

                        if (i % 2 == 0 and silence_detect_index != 0):
                            voice_end = float(data[4])
                            voice_duration = voice_end - voice_start
                            print ' *** voice_start: ' + str(voice_start) + ' voice_duration: ' + str(voice_duration)                            
                            only_voice_path = flac_path + "_only_voice_" + str(silence_detect_index) + ".flac"                             
                            only_voice_file_split_command = 'ffmpeg -ss '+ str(voice_start) +' -t '+ str(voice_duration) +' -i '+ flac_path +' ' + only_voice_path + ' -hide_banner -loglevel panic'
                            print(only_voice_file_split_command)
                            os.system(only_voice_file_split_command)

                            print("recognizing file: " + only_voice_path)
                            with io.open(only_voice_path, 'rb') as audio_file:
                                content = audio_file.read()

                            audio = types.RecognitionAudio(content=content)
                            config = types.RecognitionConfig(
                            encoding= enums.RecognitionConfig.AudioEncoding.FLAC,
                            sample_rate_hertz=16000,
                            language_code=language_code)

                            response = client.recognize(config, audio)
                            for result in response.results:
                                recognized = result.alternatives[0].transcript
                                recognition_results.append(recognized)

                        if i % 2 == 1:
                            voice_start = float(data[4])

                        silence_detect_index = silence_detect_index + 1
            continue
        else:
            continue
    print(recognition_results)    

    final_results = []

    

    with open(keywords_file) as keyWordsFile:
        for word in keyWordsFile:
            final_result = []
            word = word.rstrip()
            final_result.append(word)
            result = False
            for phrase in recognition_results:    
                if re.search(word, phrase, re.IGNORECASE):
                    result = True

            final_result.append(result)
            final_results.append(final_result)    
    pprint.pprint(final_results)

transcribe_file(sys.argv)
