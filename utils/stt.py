import subprocess
import os
import whisper
import warnings
warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*")

def transcribe_webm_with_whisper_local(webm_file, output_dir="temp_audio"):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save uploaded webm file locally
    input_path = os.path.join(output_dir, webm_file.name)
    with open(input_path, "wb") as f:
        f.write(webm_file.read())

    # Define output mp3 path
    output_path = input_path.replace(".webm", ".mp3")

    # Extract audio using ffmpeg
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vn",
        "-acodec", "libmp3lame",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Load Whisper model
    model = whisper.load_model("base")  # You can use "tiny", "small", "medium", "large"

    # Transcribe audio
    result = model.transcribe(output_path)

    # Optional: Clean up temp files
    os.remove(input_path)
    os.remove(output_path)
    print(result['text'])

    return result['text']


#model = whisper.load_model("base",device='cpu') 
#result = model.transcribe("/Users/gauravjangid/Desktop/mvp/temp_audio/response-5.mp3")
#print(result['text'])