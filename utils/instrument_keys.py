import json
from public.extract import OUTPUT_PATH

DEFAULT_ETFS_LIST = ["NIFTYBEES", "GOLDBEES"]


def get_instrument_keys(ETFS_LIST=DEFAULT_ETFS_LIST) -> dict:

    INSTRUMENT_KEYS = {}

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for instrument in data:

        if instrument.get("trading_symbol") in ETFS_LIST:

            INSTRUMENT_KEYS[instrument.get("trading_symbol")] = instrument.get(
                "instrument_key"
            )

    return INSTRUMENT_KEYS
