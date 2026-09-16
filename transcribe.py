import whisper
import sys
from moviepy import *
import numpy as np

def get_subtitles(media:str, timestamp:bool=False) -> str | dict[str, str | list]:
    model = whisper.load_model("medium")
    transcribed_media = model.transcribe(media, fp16=False)

    if timestamp:
        return transcribed_media['segments']

    return transcribed_media['text']

"""
def dynamic_var(var_name:str='subtitle1', value:str='') -> str:
    #Make dynamic variable with passed string
    exec(var_name + f' = "{value}"')
    return subtitle1
"""

def format_timestamp(subtitles, start:float, end:float, font:str="resources/Florence.ttf", font_size:int=28, color:str='#fff'):
    ...
