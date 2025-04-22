import os

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    API_ID = int(os.environ.get("API_ID", 12345))  # Get this from https://my.telegram.org
    API_HASH = os.environ.get("API_HASH")
    MONGO_URI = os.environ.get("MONGO_URI")
    FILE_CHANNEL_ID = int(os.environ.get("FILE_CHANNEL_ID"))  # Your main channel with files
    TEMP_CHANNEL_ID = int(os.environ.get("TEMP_CHANNEL_ID"))  # Temp channel for expiring links
    ADMINS = list(map(int, os.environ.get("ADMINS", "").split()))
