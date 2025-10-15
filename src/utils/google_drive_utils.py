import os
from googleapiclient.http import MediaIoBaseDownload


# function to print list all audio files in Google Drive
def list_audio_files(service, folder_id: str) -> str:
    query = f"'{folder_id}' in parents and (mimeType contains 'audio/' or name contains '.mp3' or name contains '.wav')"

    results = service.files().list(
        q=query,
        fields="files(id, name)"
    ).execute()

    return results.get("files", [])


# function to download audio files from Google Drive
def download_file(service, file_id, file_name: str):
    request = service.files().get_media(fileId=file_id)

    with open(file_name, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    print(f"Downloaded: {file_name}")


# function to save transcript locally
def save_transcript_locally(file_name: str, content: str) -> str:
    txt_file_name = os.path.splitext(file_name)[0] + ".txt"

    with open(txt_file_name, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Saved: {txt_file_name}")

    return txt_file_name
