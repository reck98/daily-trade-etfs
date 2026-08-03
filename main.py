from scripts.daily_trade import daily_trade
from scripts.get_portfolio_summary import get_portfolio_summary
from config.config import EXTRA_LINES
from utils.market_open import is_open
from rich import print
from datetime import datetime


def main():

    if not is_open():
        print(EXTRA_LINES)
        print(f"Market is closed today {datetime.today().strftime('%Y-%m-%d')}\n")
        print(EXTRA_LINES)
        return

    print(EXTRA_LINES)
    print(f"Executing daily_trade.py\n")
    daily_trade()

    print(EXTRA_LINES)
    print(f"Executing get_portfolio_summary.py\n")
    get_portfolio_summary()


if __name__ == "__main__":
    main()
