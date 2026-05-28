import pandas_market_calendars as mcal
from datetime import datetime
from rich import print


def is_open():

    nse = mcal.get_calendar("NSE")
    today = datetime.now().strftime("%Y-%m-%d")
    schedule = nse.schedule(start_date=today, end_date=today)

    return not schedule.empty
