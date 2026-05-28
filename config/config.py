from dotenv import load_dotenv
import os
from pathlib import Path as FilePath

load_dotenv()

ACCESS_TOKEN = str(os.getenv("ACCESS_TOKEN"))
BASE_URL = str(os.getenv("BASE_URL"))

PORTFOLIO_DIR = FilePath(r"E:\Development\PlayGround\daily-trade-upstox\portfolio")

EXTRA_LINES = "\n====================================================================================\n"

GEMINI_API_KEY = str(os.getenv("GEMINI_API_KEY"))
# GEMINI_API_SECRET = str(os.getenv("GEMINI_API_SECRET"))

