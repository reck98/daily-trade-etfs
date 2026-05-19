import requests
from datetime import datetime, timedelta
from config.config import ACCESS_TOKEN, BASE_URL

to_date = datetime.today().strftime("%Y-%m-%d")
from_date = (datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d")

headers = {"Accept": "application/json", "Authorization": f"Bearer {ACCESS_TOKEN}"}


# url = (
#     f"{BASE_URL}/historical-candle/"
#     f"{INSTRUMENT_KEY}/days/1/"
#     f"{to_date}/{from_date}"
# )


def get_candles_data(INSTRUMENT_KEYS, to_date=to_date, from_date=from_date):

    candles_data = {}

    for instrument_key in INSTRUMENT_KEYS.values():

        url = (
            f"{BASE_URL}/historical-candle/"
            f"{instrument_key}/days/1/"
            f"{to_date}/{from_date}"
        )

        response = requests.get(url, headers=headers)

        candles_data[instrument_key] = response.json()

    return candles_data


def make_trades(candles_data):

    trades = {}

    for candle_data in candles_data:

        print(candle_data)
        break
