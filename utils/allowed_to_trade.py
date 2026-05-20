from config.config import PORTFOLIO_DIR
import pandas as pd


def _normalize_date(value):
    parsed_date = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed_date):
        return None

    return parsed_date.strftime("%Y-%m-%d")


def allowed_to_trade(symbol, today_date):

    file_path = PORTFOLIO_DIR / f"{symbol}.csv"

    normalized_today = _normalize_date(today_date)

    if normalized_today is None:
        print(f"Invalid trade date for {symbol}: {today_date}")
        return False

    if not file_path.exists():
        return True

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return True
    except Exception as exc:
        print(f"Could not read portfolio file for {symbol}: {file_path} ({exc})")
        return False

    if df.empty:
        return True

    if "date" not in df.columns:
        print(
            f"Portfolio file for {symbol} is missing required 'date' column: {file_path}"
        )
        return False

    traded_dates = df["date"].apply(_normalize_date)

    return normalized_today not in set(traded_dates.dropna())
