from scripts.daily_trade import ETFS_LIST
from config.config import PORTFOLIO_DIR, EXTRA_LINES
import pandas as pd
from datetime import datetime
import pyxirr
from utils.get_data import get_data
from utils.instrument_keys import get_instrument_keys
from rich import print


def calculate_xirr(transactions):

    try:

        if len(transactions) < 2:

            return 0.0

        sorted_transactions = sorted(transactions, key=lambda x: x[0])

        return round(pyxirr.xirr(sorted_transactions) * 100, 2)

    except Exception:

        return 0.0


def get_portfolio_summary():

    summary_rows = []

    portfolio_transactions = []

    portfolio_total_investment = 0

    portfolio_current_value = 0

    portfolio_total_invested_today = 0

    summary_taken_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    today_date = datetime.now().strftime("%Y-%m-%d")

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

        if symbol not in market_data:

            continue

        current_price = market_data[symbol]["today_price"]

        total_current_value = round(current_price * total_shares, 2)

        pnl = round(total_current_value - total_amount, 2)

        pnl_pct = round((pnl / total_amount) * 100, 2)

        invested_today = 0

        transactions = []

        for _, row in df.iterrows():

            transaction_date = datetime.fromisoformat(row["date"])

            transaction_amount = row["total_amount"]

            transactions.append((transaction_date, -transaction_amount))

            portfolio_transactions.append((transaction_date, -transaction_amount))

            if transaction_date.strftime("%Y-%m-%d") == today_date:

                invested_today += transaction_amount

        transactions.append((datetime.now(), total_current_value))

        portfolio_total_investment += total_amount

        portfolio_current_value += total_current_value

        portfolio_total_invested_today += invested_today

        portfolio_xirr = calculate_xirr(transactions)

        summary_rows.append(
            {
                "instrument": symbol,
                "total_shares": total_shares,
                "avg_buy_price": avg_buy_price,
                "current_price": current_price,
                "invested_today": round(invested_today, 2),
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

    portfolio_pnl = round(portfolio_current_value - portfolio_total_investment, 2)

    portfolio_pnl_pct = round((portfolio_pnl / portfolio_total_investment) * 100, 2)

    portfolio_transactions.append((datetime.now(), portfolio_current_value))

    overall_portfolio_xirr = calculate_xirr(portfolio_transactions)

    summary_df = pd.DataFrame(summary_rows)

    print(EXTRA_LINES)

    print(f"Portfolio Summary Taken At: " f"{summary_taken_date}")

    print()

    print(summary_df.to_string(index=False))

    print()

    print("=" * 80)

    print(f"TOTAL INVESTED TODAY   : " f"{round(portfolio_total_invested_today, 2)}")

    print(f"TOTAL INVESTMENT       : " f"{round(portfolio_total_investment, 2)}")

    print(f"CURRENT PORTFOLIO VALUE: " f"{round(portfolio_current_value, 2)}")

    print(f"TOTAL PNL              : " f"{portfolio_pnl}")

    print(f"TOTAL PNL %            : " f"{portfolio_pnl_pct}%")

    print(f"PORTFOLIO XIRR         : " f"{overall_portfolio_xirr}%")

    print(EXTRA_LINES)

    summary_file = PORTFOLIO_DIR / "summary.csv"

    with open(summary_file, "a", encoding="utf-8") as f:

        f.write("\n")

        f.write("=" * 100)

        f.write("\n")

        f.write(f"SUMMARY_TAKEN_DATE," f"{summary_taken_date}\n")

        summary_df.to_csv(f, index=False)

        f.write("\n")

        f.write(
            f"TOTAL_INVESTED_TODAY," f"{round(portfolio_total_invested_today, 2)}\n"
        )

        f.write(f"TOTAL_INVESTMENT," f"{round(portfolio_total_investment, 2)}\n")

        f.write(f"CURRENT_PORTFOLIO_VALUE," f"{round(portfolio_current_value, 2)}\n")

        f.write(f"TOTAL_PNL," f"{portfolio_pnl}\n")

        f.write(f"TOTAL_PNL_PERCENT," f"{portfolio_pnl_pct}\n")

        f.write(f"PORTFOLIO_XIRR," f"{overall_portfolio_xirr}\n")

        f.write("\n\n")
