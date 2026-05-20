from datetime import datetime
from config.config import EXTRA_LINES, PORTFOLIO_DIR

import math
import pandas as pd
from pathlib import Path


def process_trade(trading_symbol,today_date, yesterday_date ,today_price, yesterday_price, base_price=1000):

    # today_date = datetime.now().strftime("%Y-%m-%d")
    
    if today_price <= 0 or yesterday_price <= 0:
        print(f"Invalid price data for {trading_symbol}")
        return

    pct_change = ((today_price - yesterday_price) / yesterday_price) * 100

    if pct_change >= 0:

        print(EXTRA_LINES)
        print(f"No trade for {trading_symbol}")
        print(f"Date                : {today_date}")
        print(f"Today Price         : {today_price}")
        print(f"Yesterday Price     : {yesterday_price}")
        print(f"Pct Change          : {pct_change:.2f}%")
        print(EXTRA_LINES)

        return


    amount_to_invest = base_price * abs(pct_change)

    shares_bought = math.ceil(amount_to_invest / today_price)

    total_amount = shares_bought * today_price

    print(EXTRA_LINES)

    print(f"Trade for {trading_symbol}")

    print(f"Date                : {today_date}")
    print(f"Today Price         : {today_price}")
    print(f"Yesterday Price     : {yesterday_price}")
    print(f"Pct Change          : {pct_change:.2f}%")
    print(f"Shares Bought       : {shares_bought}")
    print(f"Total Invested      : {total_amount:.2f}")

    portfolio_path = Path(PORTFOLIO_DIR)

    portfolio_path.mkdir(parents=True, exist_ok=True)

    file_path = portfolio_path / f"{trading_symbol}.csv"

    trade_data = pd.DataFrame(
        [
            {
                "date": today_date,
                "buy_price": today_price,
                "shares_bought": shares_bought,
                "total_amount": round(total_amount, 2),
            }
        ]
    )

    if file_path.exists():

        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, trade_data], ignore_index=True)

    else:
        updated_df = trade_data

    updated_df.to_csv(file_path, index=False)

    print(f"Trade saved -> {file_path}")

    print(EXTRA_LINES)

    return
