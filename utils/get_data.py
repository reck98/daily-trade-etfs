from config.config import ACCESS_TOKEN
import requests
from urllib.parse import quote
from datetime import datetime, timedelta

BASE_URL = "https://api.upstox.com"


headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}


today_date = datetime.now().strftime("%Y-%m-%d")

from_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")


def get_data(instrument_key, symbol):

    result = {}

    encoded_key = quote(instrument_key)

    # =====================================
    # HISTORICAL API
    # =====================================

    historical_url = (
        f"{BASE_URL}/v3/historical-candle/"
        f"{encoded_key}/days/1/"
        f"{today_date}/{from_date}"
    )

    historical_response = requests.get(historical_url, headers=headers)

    if historical_response.status_code != 200:

        print(f"Historical API failed for {symbol}")

        return result

    historical_data = historical_response.json()

    candles = historical_data["data"]["candles"]

    if len(candles) < 1:

        print(f"No candle data for {symbol}")

        return result

    latest_candle = candles[0]

    yesterday_date = latest_candle[0]

    yesterday_price = latest_candle[4]

    # =====================================
    # LTP API
    # =====================================

    ltp_url = f"{BASE_URL}/v3/market-quote/ltp" f"?instrument_key={encoded_key}"

    ltp_response = requests.get(ltp_url, headers=headers)

    if ltp_response.status_code != 200:

        print(f"LTP API failed for {symbol}")

        return result

    ltp_data = ltp_response.json()

    market_data = next(iter(ltp_data["data"].values()))

    today_price = market_data["last_price"]

    result[symbol] = {
        "today_date": datetime.now().strftime("%Y-%m-%d"),
        "today_price": today_price,
        "yesterday_date": yesterday_date,
        "yesterday_price": yesterday_price,
    }

    return result
