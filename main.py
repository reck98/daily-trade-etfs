from scripts.daily_trade import daily_trade
from scripts.get_portfolio_summary import get_portfolio_summary
from config.config import EXTRA_LINES


def main():

    print(EXTRA_LINES)
    print(f"Executing daily_trade.py\n")
    daily_trade()

    print(EXTRA_LINES)
    print(f"Executing get_portfolio_summary.py\n")
    get_portfolio_summary()


if __name__ == "__main__":
    main()
