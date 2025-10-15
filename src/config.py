import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("API_KEY")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
FOLDER_ID = os.getenv("FOLDER_ID")
