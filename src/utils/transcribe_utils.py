import whisper
import os
import shutil
import tempfile


def transcribe_audio(filename: str, language="Ukrainian") -> str:
    """
    transcribe audio file using Whisper model
    """
    print(f"Transcription {filename} {language}...")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    if os.path.getsize(filename) == 0:
        raise ValueError(f"File is empty: {filename}")

    # create temp file
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, os.path.basename(filename).replace(" ", "_"))

    shutil.copy(filename, temp_path)

    model = whisper.load_model("medium")

    try:
        result = model.transcribe(
            temp_path,
            language=language,
            verbose=False
        )
    except Exception as e:
        print(f"Whisper error: {e}")
        raise
    finally:
        # delete temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return result.get("text", "").strip()
