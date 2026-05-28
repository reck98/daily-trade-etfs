from utils.process_trades import process_trade
from utils.instrument_keys import get_instrument_keys
from utils.get_data import get_data
from config.config import EXTRA_LINES
from utils.allowed_to_trade import allowed_to_trade
from rich import print

ETFS_LIST = [
    "SILVERBEES",
    "GOLDETF",
    "NIFTYBEES",
    "NEXT50IETF",
    "HNGSNGBEES",
    "MID150BEES",
    "MON100",
    "MAFANG",
    "MOM30IETF",
    "HDFCSML250",
]


def daily_trade():

    instrument_keys = get_instrument_keys(ETFS_LIST=ETFS_LIST)

    # print(instrument_keys)s
    total_amount_invested = 0

    for symbol, key in instrument_keys.items():
        data = get_data(key, symbol)

        if data:
            if allowed_to_trade(symbol, data[symbol]["today_date"]):
                amount = process_trade(
                    symbol,
                    data[symbol]["today_date"],
                    data[symbol]["yesterday_date"],
                    data[symbol]["today_price"],
                    data[symbol]["yesterday_price"],
                )

                if amount:
                    total_amount_invested += amount
                
            else:
                print(EXTRA_LINES)
                print(f"Already traded for {symbol} today")
                print(EXTRA_LINES)

    print(EXTRA_LINES)
    print(f"Total amount invested Today: {total_amount_invested}")
    print(EXTRA_LINES)
    
    return
