from config.config import ACCESS_TOKEN, BASE_URL, EXTRA_LINES
import requests
from datetime import datetime, timedelta
from urllib.parse import quote

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}

today_date = datetime.now().strftime("%Y-%m-%d")

from_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")


def get_data(instrument_key, symbol) -> dict:

    result = {}

    encoded_key = quote(instrument_key)
    url = (
        f"{BASE_URL}/historical-candle/"
        f"{encoded_key}/days/1/"
        f"{today_date}/{from_date}"
    )
    
    # print(url)

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()

        candles = data["data"]["candles"]

        if len(candles) < 2:

            print(f"Not enough candle data for {symbol}")
            return result

        today_candle = candles[0]

        yesterday_candle = candles[1]
        
        if today_candle[0] != today_date or yesterday_candle[0] != (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"):
            print(f"Invalid candle data for {symbol}")
            return result

        result[symbol] = {
            "today_date": today_candle[0],
            "today_price": today_candle[4],
            "yesterday_date": yesterday_candle[0],
            "yesterday_price": yesterday_candle[4],
        }
        
        # print(EXTRA_LINES)
        # print(result[symbol])
        # print(EXTRA_LINES)

    else:

        print(f"Error fetching {symbol}")

        print(response.status_code)

        print(response.text)

    return result
