import os

from dotenv import load_dotenv
from func.core import load_msg

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_API_URL = os.getenv("BASE_API_URL")

CHANNEL_ID = os.getenv("CHANNEL_ID")
DEBUG_MODE = os.getenv("DEBUG_MODE")

THEREAD_CHANNEL = os.getenv("THEREAD_CHANNEL")
THEREAD_CHANNEL_ID = os.getenv("THEREAD_CHANNEL_ID")

DEBUG_CHANNEL_ID = os.getenv("DEBUG_CHANNEL_ID")
DEBUG_THEREAD_CHANNEL_ID = os.getenv("DEBUG_THEREAD_CHANNEL_ID")

DIR_FILES_SCRIPT = os.getenv("DIR_FILES_SCRIPT")

USER_OLT = os.getenv("USER_OLT")
PASS_OLT = os.getenv("PASS_OLT")

information = {
    'status': 0
}

LANGUAGE = 'ptbr'
MSG = load_msg(LANGUAGE, __file__)