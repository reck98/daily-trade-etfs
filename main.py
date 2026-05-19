from scripts.daily_trade import get_candles_data, make_trades
from utils.instrument_keys import get_instrument_keys


ETFS_LIST = ["SILVERBEES", "GOLDBEES", "NIFTYBEES"]
INSTRUMENT_KEYS = get_instrument_keys(ETFS_LIST)

candles_data = get_candles_data(INSTRUMENT_KEYS)

make_trades(candles_data)