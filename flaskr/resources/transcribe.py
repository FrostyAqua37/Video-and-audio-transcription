from faster_whisper import WhisperModel
from pprint import pprint
import re
import time

class Transcribe():
    def __init__(self, model_type:str='large-v2'):
        self.model = WhisperModel(model_type, device='cpu', compute_type='int8')    #Whisper model object.
        self.subtitles = '' #Variable to store transcribed subtitles.
        self.transcribed_text = [] #List with dictionaries to store formatted subtitles.

    def get_subtitles(self, media):
        #Transcribes media with WhisperModel
        self.subtitles, _ = self.model.transcribe(media, beam_size=5)

    def format_subtitles(self):
        pattern = '^[\\w.,!? ]*$'  #Regex pattern for letters, numbers, whitespace and punctation characters.
        id = 1
        
        for subtitle in self.subtitles:
            subtitle.text = subtitle.text.strip()
        
            if re.search(pattern, subtitle.text) is None:
                #Skips any characters outside the pattern above.
                continue

            start = self.format_timestamp(subtitle.start)
            end = self.format_timestamp(subtitle.end)
                    
            #Adds a dictionary of id, timestamp of start and end and transcribed text into the list.
            self.transcribed_text.append({
                'id': id,
                'timestamp': f'[{start} — {end}]', #Combines start and end time of current subtitle into one
                'text': subtitle.text
            })
            id += 1    

    def format_timestamp(self, seconds:int) -> str:
        #Formats seconds into HH:MM:SS or MM:SS if total seconds is less than an hour.
        if seconds < 3600:
            return time.strftime('%M:%S', time.gmtime(seconds))
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def transcribe(self, media):
        #Runs methods necessary to transcribe and format subtitles.
        self.get_subtitles(media)
        self.format_subtitles()
        return self.transcribed_text

def main():
    video_transcriber = Transcribe('resources/files/youtube-audio.mp4', 'video')
    video_transcriber.transcribe()
    video_transcriber.format_subtitles()
    pprint(video_transcriber.transcribed_text)

if __name__ == '__main__':
    main()

