import time
import requests
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


def _execute_trade(symbol, data, current_total):
    """Process trade for symbol if data is valid and trading is permitted."""
    if not data or symbol not in data:
        return current_total

    if allowed_to_trade(symbol, data[symbol]["today_date"]):
        amount = process_trade(
            symbol,
            data[symbol]["today_date"],
            data[symbol]["yesterday_date"],
            data[symbol]["today_price"],
            data[symbol]["yesterday_price"],
        )

        if amount:
            current_total += amount

    else:
        print(EXTRA_LINES)
        print(f"Already traded for {symbol} today")
        print(EXTRA_LINES)

    return current_total


def daily_trade():
    instrument_keys = get_instrument_keys(ETFS_LIST=ETFS_LIST)
    total_amount_invested = 0
    waitlist = []

    # --- Primary Pass ---
    for symbol, key in instrument_keys.items():
        try:
            data = get_data(key, symbol)
            total_amount_invested = _execute_trade(symbol, data, total_amount_invested)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            print(EXTRA_LINES)
            print(f"[bold yellow]Connection timeout/error for {symbol}: {exc}. Adding to waitlist.[/bold yellow]")
            print(EXTRA_LINES)
            waitlist.append((symbol, key))
        except Exception as exc:
            print(EXTRA_LINES)
            print(f"[bold red]Unexpected error fetching data for {symbol}: {exc}[/bold red]")
            print(EXTRA_LINES)

    # --- Waitlist Pass ---
    if waitlist:
        print(EXTRA_LINES)
        print(f"[bold cyan]Processing {len(waitlist)} waitlisted ETF(s)...[/bold cyan]")
        print(EXTRA_LINES)

        # Delays: Attempt 1: immediate (0s), Attempt 2: 10s wait, Attempt 3: 30s wait
        retry_delays = [0, 10, 30]

        for symbol, key in waitlist:
            succeeded = False
            for attempt, delay in enumerate(retry_delays, start=1):
                if delay > 0:
                    print(f"[yellow]Waiting {delay}s before retry attempt {attempt} for {symbol}...[/yellow]")
                    time.sleep(delay)
                try:
                    print(f"[cyan]Attempt {attempt} for waitlisted {symbol}...[/cyan]")
                    data = get_data(key, symbol)
                    total_amount_invested = _execute_trade(symbol, data, total_amount_invested)
                    succeeded = True
                    break
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
                    print(f"[yellow]Attempt {attempt} failed for {symbol}: {exc}[/yellow]")
                except Exception as exc:
                    print(f"[red]Attempt {attempt} encountered unexpected error for {symbol}: {exc}[/red]")
                    break

            if not succeeded:
                print(EXTRA_LINES)
                print(f"[bold red]Failed to connect for {symbol} after all {len(retry_delays)} attempts. Skipping to next.[/bold red]")
                print(EXTRA_LINES)

    print(EXTRA_LINES)
    print(f"Total amount invested Today: {total_amount_invested}")
    print(EXTRA_LINES)

    return
