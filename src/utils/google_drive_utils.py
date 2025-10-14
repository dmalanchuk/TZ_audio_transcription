from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from src import config
import os

# connect to Google Drive
credentials = service_account.Credentials.from_service_account_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive']
)
service = build('drive', 'v3', credentials=credentials)


# function to print list all audio files in Google Drive
def list_audio_files():
    results = service.files().list(fields="files(id, name)").execute()
    for f in results.get('files', []):
        print(f['name'])


def download_audio_file(file_id: str, file_name: str) -> str:
    request = service.files().get_media(fileId=file_id)
    with open(file_name, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        return file_name


def upload_text_file(local_path: str, folder_id: str) -> str:
    file_metadata = {
        'name': os.path.basename(local_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(local_path, mimetype='text/plain')
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return f"upload to: {folder_id} success"
