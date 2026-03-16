import os
import pandas as pd
from datetime import timedelta
from src.utils_io import load_config, write_parquet

def main() -> None:
    cfg = load_config()
    processed = cfg["paths"]["processed"]
    features_path = cfg["paths"]["features"]

    customers = pd.read_parquet(os.path.join(processed, "customers.parquet"))
    subs = pd.read_parquet(os.path.join(processed, "subscriptions.parquet"))
    invoices = pd.read_parquet(os.path.join(processed, "invoices.parquet"))
    usage = pd.read_parquet(os.path.join(processed, "daily_usage.parquet"))

    # Ensure datetime types
    for col in ["start_date", "end_date"]:
        subs[col] = pd.to_datetime(subs[col])

    invoices["issued_at"] = pd.to_datetime(invoices["issued_at"])
    usage["usage_date"] = pd.to_datetime(usage["usage_date"])

    # Label: churned if status == 'canceled'
    subs["is_churned"] = (subs["status"] == "canceled").astype(int)

    # 30‑day usage aggregates
    max_date = usage["usage_date"].max()
    window_start = max_date - timedelta(days=30)

    recent_usage = usage[usage["usage_date"].between(window_start, max_date)]
    agg_usage = (
        recent_usage
        .groupby("subscription_id")
        .agg(
            requests_30d=("requests", "sum"),
            storage_gb_30d=("storage_gb", "mean"),
            errors_30d=("errors", "sum"),
        )
        .reset_index()
    )

    # Monetary: total invoice amount last 90 days
    inv_window_start = max_date - timedelta(days=90)
    recent_invoices = invoices[invoices["issued_at"].between(inv_window_start, max_date)]
    agg_invoices = (
        recent_invoices
        .groupby("subscription_id")
        .agg(
            amount_90d=("amount", "sum"),
            invoices_90d=("invoice_id", "count"),
        )
        .reset_index()
    )

    # Join everything
    features = (
        subs
        .merge(customers, on="customer_id", how="left")
        .merge(agg_usage, on="subscription_id", how="left")
        .merge(agg_invoices, on="subscription_id", how="left")
    )

    # Simple recency feature
    features["subscription_age_days"] = (max_date - features["start_date"]).dt.days

    write_parquet(features, os.path.join(features_path, "churn_features.parquet"))

if __name__ == "__main__":
    main()
