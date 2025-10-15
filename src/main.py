from google.oauth2 import service_account
from googleapiclient.discovery import build
import ssl
import os
from pathlib import Path

from src import config
from src.utils.transcribe_utils import transcribe_audio
from src.utils.google_drive_utils import (
    list_audio_files,
    download_file,
    save_transcript_locally,
)

from src.utils.excel_utils import write_to_excel, analyze_transcript

# off ssl for local testing
ssl._create_default_https_context = ssl._create_unverified_context

# Google Drive scope
SCOPES = ["https://www.googleapis.com/auth/drive"]

# path for downloaded audio files
BASE_DIR = Path(__file__).parent
DOWNLOAD_DIR = BASE_DIR / "files"


def main():
    """main function to process audio files from Google Drive and save transcripts locally."""
    folder_id = config.FOLDER_ID

    creds = service_account.Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    # audio files form Google Drive
    audio_files = list_audio_files(service, folder_id)
    total = len(audio_files)
    print(f"Find {total} audio files in Google Drive")

    if total == 0:
        print("no audio files found")
        return

    # limit files to processing for testing
    try:
        limit = int(input(f"How many files to process (1–{total})? ").strip())
    except ValueError as ve:
        print(f"incorrect input: {ve}, using all files")
        limit = total

    limit = max(1, min(limit, total))
    files_to_process = audio_files[:limit]

    print(f"We start processing {limit} files")

    # main for loop with enumerating
    for idx, file in enumerate(files_to_process, start=1):
        file_id, name = file["id"], file["name"]
        print(f"\n[{idx}/{limit}] processing {name}")

        file_path = os.path.join(DOWNLOAD_DIR, name)

        # download audio file from Google Drive
        download_file(service, file_id, file_path)
        print(f"Downloaded to: {file_path}")

        # transcribe audio files and save transcript locally
        text = transcribe_audio(file_path)
        save_transcript_locally(file_path, text)

        # analyze transcript and write to Excel
        row_data = analyze_transcript(text)
        write_to_excel(row_data)
        print(f"Success: {name}\n")

    print("all files processed")


if __name__ == "__main__":
    main()
