from dotenv import load_dotenv
import os

load_dotenv()


ACCESS_TOKEN = str(os.getenv("ACCESS_TOKEN"))
BASE_URL = str(os.getenv("BASE_URL"))
