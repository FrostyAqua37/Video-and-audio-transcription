import whisper
import sys
from moviepy import *
import numpy as np

def get_subtitles(media:str, timestamp:bool=False) -> str | dict[str, str | list]:
    model = whisper.load_model("large-v3")
    transcribed_media = model.transcribe(media, fp16=False)

    if timestamp:
        #Returns transcribed text with timestamp if 'timestamp=True'
        return transcribed_media['segments']

    #Returns only transcribed text
    return transcribed_media['text']

def format_timestamp(subtitle:str, font:str="resources/BebasNeue-Regular.ttf", font_size:int=28, color:str='#fff'):
    #Formats transcribed text to fit video.
    return TextClip(
            font=font,
            text=subtitle,
            font_size=font_size,
            color=color,
            text_align='center'
            )

#subtitles = get_subtitles(sys.argv[1], timestamp=True)  #Gets video file location from terminal and passes it to function
#subtitle_list = []

"""
for subtitle in subtitles:
    #Loops through all the transcribed text and sets start and end duration. 
    subtitle_list.append(format_timestamp(subtitle=subtitle['text']))   
    subtitle_list[subtitle['id']].with_start(subtitle['start']).with_end(subtitle['end'])   
    subtitle_list[subtitle['id']].with_position(('center', 'bottom'))

media = VideoFileClip('resources/youtube-audio.mp4')
media.with_start(1).with_end(184.26)
subtitle_list.insert(0, media)
video_transcribed = CompositeVideoClip(subtitle_list)
video_transcribed.preview(fps=20)
"""

media = VideoFileClip(sys.argv[1])
media = media.subclipped(1, 60)
media.preview()
