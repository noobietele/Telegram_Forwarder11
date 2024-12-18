import logging
import json
import requests
from os import getenv, path, makedirs

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv(".env")

logging.basicConfig(
    format="[ %(asctime)s: %(levelname)-8s ] %(name)-20s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

httpx_logger = logging.getLogger('httpx')
httpx_logger.setLevel(logging.WARNING)

# GitHub personal access token (set directly in the code)
GITHUB_TOKEN = "your_personal_access_token_here"

# Define the URL for downloading the JSON file
config_url = "https://example.com/path/to/chat_list.json"

# Define the directory where the downloaded file will be saved
download_directory = "downloads"

# Define the local path where the downloaded file will be saved
config_name = "chat_list.json"
config_path = path.join(download_directory, config_name)

# Create the directory if it doesn't exist
if not path.exists(download_directory):
    makedirs(download_directory)
    
# Check if GitHub token is provided
if not GITHUB_TOKEN:
    LOGGER.error("No GITHUB_TOKEN provided! Exiting...")
    exit(1)

# Fetch the JSON file from the private GitHub repository using the token
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

try:
    response = requests.get(config_url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    # Save the content of the JSON file to the local path
    with open(config_path, "w") as file:
        file.write(response.text)
    LOGGER.info("chat_list.json downloaded successfully!")
except requests.RequestException as e:
    LOGGER.error(f"Error downloading chat_list.json: {e}")
    exit(1)

# Load the downloaded JSON file
if not path.isfile(config_path):
    LOGGER.error("No chat_list.json config file found! Exiting...")
    exit(1)

with open(config_path, "r") as data:
    CONFIG = json.load(data)

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    LOGGER.error("No BOT_TOKEN token provided!")
    exit(1)
OWNER_ID = int(getenv("OWNER_ID", "0"))
REMOVE_TAG = getenv("REMOVE_TAG", "False") in {"true", "True", 1}

bot = ApplicationBuilder().token(BOT_TOKEN).build()
