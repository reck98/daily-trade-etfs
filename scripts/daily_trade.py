from utils.process_trades import process_trade
from utils.instrument_keys import get_instrument_keys
from utils.get_data import get_data
from config.config import EXTRA_LINES
from utils.allowed_to_trade import allowed_to_trade

ETFS_LIST = ["SILVERBEES", "GOLDBEES", "NIFTYBEES"]


def daily_trade():

    instrument_keys = get_instrument_keys(ETFS_LIST=ETFS_LIST)

    for symbol, key in instrument_keys.items():
        data = get_data(key, symbol)

        if data:
            if allowed_to_trade(symbol, data[symbol]["today_date"]):
                process_trade(
                    symbol, data[symbol]["today_price"], data[symbol]["yesterday_price"]
                )
            else:
                print(EXTRA_LINES)
                print(f"Alredy traded for {symbol} today")
                print(EXTRA_LINES)
    return
