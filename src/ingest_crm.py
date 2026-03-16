import os
import pandas as pd
from src.utils_io import load_config, read_csv, write_parquet
from src.schemas import CUSTOMERS_COLUMNS, SUBSCRIPTIONS_COLUMNS

def main() -> None:
    cfg = load_config()
    raw = cfg["paths"]["raw"]
    processed = cfg["paths"]["processed"]

    customers = read_csv(os.path.join(raw, "crm_customers.csv"))[CUSTOMERS_COLUMNS]
    subs = read_csv(os.path.join(raw, "crm_subscriptions.csv"))[SUBSCRIPTIONS_COLUMNS]

    write_parquet(customers, os.path.join(processed, "customers.parquet"))
    write_parquet(subs, os.path.join(processed, "subscriptions.parquet"))

if __name__ == "__main__":
    main()
