from config.config import ACCESS_TOKEN
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import quote
from datetime import datetime, timedelta

BASE_URL = "https://api.upstox.com"
DEFAULT_TIMEOUT = (10, 20)  # (connect timeout, read timeout) in seconds

_SESSION = None


def get_session():
    """Return a shared requests.Session with connection pooling and auth headers."""
    global _SESSION
    if _SESSION is None:
        _SESSION = requests.Session()
        _SESSION.headers.update(
            {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Accept": "application/json",
            }
        )
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
        _SESSION.mount("https://", adapter)
        _SESSION.mount("http://", adapter)
    return _SESSION


def get_data(instrument_key, symbol, session=None):
    if session is None:
        session = get_session()

    result = {}
    encoded_key = quote(instrument_key)

    today_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")

    historical_url = (
        f"{BASE_URL}/v3/historical-candle/"
        f"{encoded_key}/days/1/"
        f"{today_date}/{from_date}"
    )

    # Let Timeout and ConnectionError bubble up so caller can handle retry/waitlist
    historical_response = session.get(historical_url, timeout=DEFAULT_TIMEOUT)

    if historical_response.status_code != 200:
        print(
            f"Historical API failed for {symbol}: status {historical_response.status_code}, response: {historical_response.text}"
        )
        return result

    historical_data = historical_response.json()
    candles = historical_data.get("data", {}).get("candles", [])

    if len(candles) < 1:
        print(f"No candle data for {symbol}")
        return result

    latest_candle = candles[0]
    yesterday_date = latest_candle[0]
    yesterday_price = latest_candle[4]

    ltp_url = f"{BASE_URL}/v3/market-quote/ltp?instrument_key={encoded_key}"
    ltp_response = session.get(ltp_url, timeout=DEFAULT_TIMEOUT)

    if ltp_response.status_code != 200:
        print(
            f"LTP API failed for {symbol}: status {ltp_response.status_code}, response: {ltp_response.text}"
        )
        return result

    ltp_data = ltp_response.json()
    data_values = ltp_data.get("data", {})
    if not data_values:
        print(f"No LTP data returned for {symbol}")
        return result

    market_data = next(iter(data_values.values()))
    today_price = market_data.get("last_price", 0)

    result[symbol] = {
        "today_date": datetime.now().strftime("%Y-%m-%d"),
        "today_price": today_price,
        "yesterday_date": yesterday_date,
        "yesterday_price": yesterday_price,
    }

    return result
