import os
import subprocess
import whisper
import warnings
import logging

warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*")
logging.basicConfig(level=logging.INFO)

def transcribe_webm_with_whisper_local(webm_file, output_dir="temp_audio", model_size="base", cleanup=True) -> str:
    """
    Transcribes a .webm file using Whisper locally.

    Args:
        webm_file: Uploaded file-like object (e.g., from Streamlit).
        output_dir (str): Directory to store temporary audio files.
        model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large").
        cleanup (bool): Whether to delete temp files after transcription.

    Returns:
        str: Transcribed text.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save uploaded file
    input_path = os.path.join(output_dir, webm_file.name)
    with open(input_path, "wb") as f:
        f.write(webm_file.read())

    # Convert to mp3
    output_path = input_path.replace(".webm", ".mp3")
    ffmpeg_cmd = [
        "ffmpeg", "-i", input_path,
        "-vn", "-acodec", "libmp3lame",
        output_path
    ]
    try:
        subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg conversion failed: {e}")
        return ""

    # Load Whisper model
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(output_path)
        transcript = result.get("text", "")
        logging.info(f"Transcription complete: {transcript[:60]}...")
    except Exception as e:
        logging.error(f"Whisper transcription failed: {e}")
        transcript = ""

    # Clean up
    if cleanup:
        for path in [input_path, output_path]:
            try:
                os.remove(path)
            except OSError:
                logging.warning(f"Failed to delete temp file: {path}")

    return transcript
