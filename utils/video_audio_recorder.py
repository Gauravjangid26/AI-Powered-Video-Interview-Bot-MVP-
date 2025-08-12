import cv2
import numpy as np
import pyaudio
import wave
import os
from datetime import datetime

# Constants
FPS = 30
AUDIO_RATE = 44100
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHUNK = 1024

# Create recordings directory
recordings_dir = 'recordings'
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)

def get_valid_channels(p: pyaudio.PyAudio, device_index: int = None) -> int:
    """
    Determine the number of input channels supported by the audio device.

    Args:
        p: PyAudio instance.
        device_index: Index of the input device (None for default).

    Returns:
        int: Number of supported channels (1 for mono, 2 for stereo, etc.).
    """
    try:
        device_info = p.get_default_input_device_info() if device_index is None else p.get_device_info_by_index(device_index)
        max_channels = device_info['maxInputChannels']
        # Test 1 or 2 channels, default to 1 if 2 fails
        return 2 if max_channels >= 2 else 1
    except Exception as e:
        print(f"Error detecting channels: {e}. Defaulting to 1 channel.")
        return 1

def record_audio_video(channel: int) -> None:
    """
    Record video and audio from a webcam and microphone, saving separately.

    Args:
        channel (int): Camera channel number.

    Returns:
        None
    """
    cap = None
    out = None
    audio_stream = None
    wave_file = None
    p = None

    try:
        # Initialize video capture
        cap = cv2.VideoCapture(channel)
        if not cap.isOpened():
            raise ValueError(f"Error opening camera channel {channel}.")

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) if cap.get(cv2.CAP_PROP_FPS) > 0 else FPS

        # Initialize video writer
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_path = os.path.join(recordings_dir, f'{timestamp}_{channel}_webcam_recording.mp4')
        out = cv2.VideoWriter(
            video_path,
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (width, height)
        )

        # Initialize audio
        p = pyaudio.PyAudio()
        audio_channels = get_valid_channels(p)
        audio_path = os.path.join(recordings_dir, f'{timestamp}_{channel}_audio_recording.wav')
        audio_stream = p.open(
            format=AUDIO_FORMAT,
            channels=audio_channels,
            rate=AUDIO_RATE,
            input=True,
            frames_per_buffer=AUDIO_CHUNK
        )
        wave_file = wave.open(audio_path, 'wb')
        wave_file.setnchannels(audio_channels)
        wave_file.setsampwidth(p.get_sample_size(AUDIO_FORMAT))
        wave_file.setframerate(AUDIO_RATE)

        print(f"Recording video to {video_path} and audio to {audio_path}. Press 'q' to stop.")

        # Stream and save
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading video frame.")
                break

            audio_data = audio_stream.read(AUDIO_CHUNK, exception_on_overflow=False)

            out.write(frame)
            wave_file.writeframes(audio_data)

            cv2.imshow("Webcam - Press 'q' to quit", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error in record_audio_video: {e}")

    finally:
        # Clean up
        if cap is not None:
            cap.release()
        if out is not None:
            out.release()
        if audio_stream is not None:
            audio_stream.stop_stream()
            audio_stream.close()
        if wave_file is not None:
            wave_file.close()
        if p is not None:
            p.terminate()
        cv2.destroyAllWindows()

def main():
    record_audio_video(0)

if __name__ == "__main__":
    main()