import gzip
import shutil
from pathlib import Path as FilePath 


def extract_gz(input_path: FilePath, output_path: FilePath):
    with gzip.open(input_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


FILE_PATH = FilePath(r"E:\Development\PlayGround\daily-trade-upstox\public\NSE.json.gz")

OUTPUT_PATH = FilePath(r"E:\Development\PlayGround\daily-trade-upstox\public\NSE.json")

# extract_gz(FILE_PATH, OUTPUT_PATH)
