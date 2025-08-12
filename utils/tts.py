import os
from gtts import gTTS
from datetime import datetime
import subprocess

def text_to_speech(text: str, lang: str = "en", slow: bool = False, output_dir: str = "tts_output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    filepath = os.path.join(output_dir, filename)

    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(filepath)
        
        subprocess.run(["afplay", filepath])  # Works on macOS
    except Exception as e:
        return f"[TTS Error] {e}"

# Test
#text = "Hello! I am your AI interview assistant. Let's get started."
#mp3_path = text_to_speech(text)

#print("TTS saved at:", mp3_path)
#subprocess.run(["afplay", mp3_path])  # Works on macOS
