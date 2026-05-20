from dotenv import load_dotenv
import os
from pathlib import Path as FilePath

load_dotenv()

ACCESS_TOKEN = str(os.getenv("ACCESS_TOKEN"))
BASE_URL = str(os.getenv("BASE_URL"))

PORTFOLIO_DIR = FilePath(r"E:\Development\PlayGround\daily-trade-upstox\portfolio")

EXTRA_LINES = "\n====================================================================================\n"

