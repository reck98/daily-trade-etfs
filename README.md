# Daily Trade Upstox

A small Python script for tracking a simple ETF dip-buying strategy using Upstox market data.

Right now this is a paper-trading tool. It fetches a recent daily candle, checks the latest LTP against that reference price, and records the calculated buy in a local CSV file. It does not place live Upstox orders.

## Strategy

The script currently watches:

- `SILVERBEES`
- `GOLDETF`
- `NIFTYBEES`
- `NEXT50IETF`
- `HNGSNGBEES`
- `MID150BEES`
- `MON100`
- `MAFANG`
- `MOM30IETF`
- `HDFCSML250`

For each ETF:

1. Fetch recent daily candle data from Upstox.
2. Fetch the current LTP from Upstox.
3. Compare the current LTP with the latest historical close.
4. If the ETF is flat or up, do nothing.
5. If the ETF is down, calculate a paper buy:

```text
amount_to_invest = base_price * absolute_percentage_fall
quantity = ceil(amount_to_invest / today_price)
```

The default `base_price` is `1000`, so a 1.5% fall means roughly `1500` worth of paper buying before quantity rounding.

## Project Layout

```text
main.py                         # Runs daily trading, then portfolio summary
scripts/daily_trade.py          # ETF loop and strategy orchestration
scripts/get_portfolio_summary.py # Portfolio summary helper
utils/get_data.py               # Upstox historical candle fetch
                                # and LTP fetch
utils/instrument_keys.py        # Finds instrument keys from NSE.json
utils/process_trades.py         # Calculates and stores paper trades
utils/allowed_to_trade.py       # Prevents duplicate same-day entries
config/config.py                # Environment and local path config
public/NSE.json                 # Upstox instrument dump
```

## Setup

This project uses Python 3.12 and `uv`.

```bash
uv sync
```

Create a `.env` file in the project root:

```env
ACCESS_TOKEN=your_upstox_access_token
```

The token comes from your Upstox developer app login flow. Access tokens expire, so expect to refresh it as needed.

## Run

Run the daily workflow:

```bash
uv run python main.py
```

`main.py` does two things in order:

1. Runs `daily_trade()` to check the ETF strategy and save any new paper trades.
2. Runs `get_portfolio_summary()` to print and append the latest portfolio summary.

Paper trades are written under the configured `portfolio` directory, one CSV per ETF. Portfolio snapshots are appended to `portfolio/summary.csv`.

## Portfolio Summary

The summary script reads the paper-trade CSVs and prints:

- total shares
- average buy price
- current price
- total investment
- current value
- P&L
- P&L percentage
- XIRR

## Trade Guard

`utils/allowed_to_trade.py` prevents duplicate entries for the same ETF and date. It checks the existing CSV history and refuses to trade if that date is already present.

The guard is intentionally conservative:

- missing CSV: trade allowed
- empty CSV: trade allowed
- same date already present: trade blocked
- missing `date` column or unreadable CSV: trade blocked

## Current Limitations

- This does not place real orders.
- There is no brokerage, slippage, tax, or liquidity model.
- Portfolio files are simple CSVs, not a database.
- Paths in config are currently local-machine oriented.
- Upstox historical candle handling should be reviewed carefully before using this for live decisions.

Treat this as a personal automation script and research ledger, not a production trading system.
