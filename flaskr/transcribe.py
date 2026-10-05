from faster_whisper import WhisperModel
from pprint import pprint
import json
import re

class MediaTranscriber:
    def __init__(self, media:str, type:str, model_type:str='large-v2',):
        self.media = media  #Filename.
        self.type = type    #Filetype.
        self.model = WhisperModel(model_type, device='cpu', compute_type='int8')    #Whisper model object.
        self.subtitles = '' #Variable to store transcribed subtitles.
        self.transcribed_text = [] #List with dictionaries to store formatted subtitles.
        
    def transcribe(self):
        #Transcribes media with WhisperModel
        self.subtitles, _ = self.model.transcribe(self.media, beam_size=5)

    def format_subtitles(self):
        pattern = '^[\\w.,!? ]*$'  #Regex pattern for letters, numbers, whitespace and punctation characters.
        id = 1
        
        for subtitle in self.subtitles:
            subtitle.text = subtitle.text.strip()
        
            if re.search(pattern, subtitle.text) is None:
                #Skips any characters outside the pattern above.
                continue
                    
            #Adds a dictionary of id, timestamp of start and end and transcribed text into the list.
            self.transcribed_text.append({
                'id': id,
                'timestamp': f'[{round(subtitle.start, 2)} - {round(subtitle.end, 2)}]', #Combines start and end time of current subtitle into one
                'text': subtitle.text
            })
            id += 1    

        return self.transcribed_text
        
    def save(self):
        with open('resources/files/subtitles.json', 'w') as f:
            #Converts list of dictionaries into json file.
            json.dump(self.transcribed_text, f, indent=4)

def main():
    video_transcriber = MediaTranscriber('resources/files/youtube-audio.mp4', 'video')
    video_transcriber.transcribe()
    video_transcriber.format_subtitles()
    pprint(video_transcriber.transcribed_text)

if __name__ == '__main__':
    main()

