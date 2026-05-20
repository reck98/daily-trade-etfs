from scripts.daily_trade import ETFS_LIST
from config.config import PORTFOLIO_DIR, EXTRA_LINES
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.optimize import newton
from utils.get_data import get_data
from utils.instrument_keys import get_instrument_keys


def xirr(transactions):

    def xnpv(rate):

        first_date = transactions[0][0]

        total = 0

        for date, amount in transactions:

            days = (date - first_date).days

            total += amount / ((1 + rate) ** (days / 365))

        return total

    try:

        return round(newton(xnpv, 0.1) * 100, 2)

    except:

        return 0.0


def get_portfolio_summary():

    summary_rows = []

    summary_taken_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    instrument_keys = get_instrument_keys(ETFS_LIST=ETFS_LIST)
    for symbol in ETFS_LIST:

        file_path = PORTFOLIO_DIR / f"{symbol}.csv"

        if not file_path.exists():

            continue

        df = pd.read_csv(file_path)

        if df.empty:

            continue

        total_amount = df["total_amount"].sum()

        total_shares = df["shares_bought"].sum()

        avg_buy_price = round(total_amount / total_shares, 2)

        market_data = get_data(instrument_keys[symbol], symbol)

        current_price = market_data[symbol]["today_price"]

        total_current_value = round(current_price * total_shares, 2)

        pnl = round(total_current_value - total_amount, 2)

        pnl_pct = round((pnl / total_amount) * 100, 2)

        transactions = []

        for _, row in df.iterrows():

            transactions.append(
                (datetime.fromisoformat(row["date"]), -row["total_amount"])
            )

        transactions.append((datetime.now(), total_current_value))

        portfolio_xirr = xirr(transactions)

        summary_rows.append(
            {
                "instrument": symbol,
                "total_shares": total_shares,
                "avg_buy_price": avg_buy_price,
                "current_price": current_price,
                "total_investment": round(total_amount, 2),
                "current_value": total_current_value,
                "pnl": pnl,
                "pnl_pct": pnl_pct,
                "xirr": portfolio_xirr,
            }
        )

    if not summary_rows:

        print("No portfolio data found")

        return

    summary_df = pd.DataFrame(summary_rows)

    print(EXTRA_LINES)

    print(f"Portfolio Summary Taken At: {summary_taken_date}")

    print(summary_df.to_string(index=False))

    print(EXTRA_LINES)

    summary_file = PORTFOLIO_DIR / "summary.csv"

    with open(summary_file, "a", encoding="utf-8") as f:

        f.write("\n")
        f.write("=" * 80)
        f.write("\n")

        f.write(f"SUMMARY_TAKEN_DATE,{summary_taken_date}\n")

        summary_df.to_csv(f, index=False)

        f.write("\n\n")
