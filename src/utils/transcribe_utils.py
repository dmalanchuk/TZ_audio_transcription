import whisper

model = whisper.load_model("medium")


def transcribe_audio(filename):
    """Transcription in Ukrainian, model: medium, Whisper"""
    print(f"Transcription {filename} Ukrainian...")

    result = model.transcribe(
        filename,
        language="uk",  # UA language
        fp16=False,
        temperature=0.0,  # for stable results
        verbose=False
    )

    print(f"Getting text from {filename}")

    return result["text"]
