#import whisper
from faster_whisper import WhisperModel
import json
import re

def get_subtitles(media:str, timestamp:bool=False) -> str | dict[str, str | list]:
    model = WhisperModel('large-v2', device='cpu', compute_type='int8')
    segments, info = model.transcribe(media, beam_size=5)

    if timestamp:
        #Returns transcribed text with timestamps
        return segments

    #Returns only transcribed text
    return info

def get_metadata(media:str):
    ...

def subtitles_to_json(subtitles):
    transcribed_text:list[dict[str, str]] = []
    pattern = '^[\w.,!?]+$'

    for subtitle in subtitles:
        if re.search(pattern, subtitle.text) is not None:
            #Adds a dictionary of id, timestamp of start and end and transcribed text into the list.
            transcribed_text.append({
                'id': subtitle.id,
                'start': f'{subtitle.start:.2f}',
                'end': f'{subtitle.end:.2f}',
                'text': subtitle.text
            })
        else:
            #Skips any characters outside the pattern above.
            continue

    #Returns list of dictionaries in JSON format.
    return json.dumps(transcribed_text)

segments = get_subtitles('resources/files/youtube-audio.mp4', True)

print(subtitles_to_json(segments))
