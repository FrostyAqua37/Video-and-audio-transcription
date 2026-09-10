import whisper
import sys

media = sys.argv[1]
model = whisper.load_model("base")
transcribed_media = model.transcribe(media, fp16=False)

print(transcribed_media['segments'])