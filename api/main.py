from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pyttsx3

# Instantiation of clients
actor = pyttsx3.init()
app: FastAPI = FastAPI()

# Property Sets
words_per_minute: int = 200
#actor.setProperty('language', 'german')
actor.setProperty('rate', words_per_minute)
actor.setProperty('volume', 5.0)

# Audio Functions
def text_to_speech(text: str, file_output: str):
    actor.save_to_file(text , file_output)
    actor.runAndWait()
    return file_output


# API
@app.get(path="/")
def read_root():
    return {"API": "alive"}

@app.get(path="/api/generate_audio")
async def read_item(text: str):
    if text == "": return None;
    
    generated_audio_file = text_to_speech(text=text, file_output=".\\output.mp3")
    
    def iterfile():
        with open(generated_audio_file, mode="rb") as file_like:
            yield from file_like  
    
    return StreamingResponse(content=iterfile(), media_type="audio/mpeg")
