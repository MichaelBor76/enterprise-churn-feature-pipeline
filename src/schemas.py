CUSTOMERS_COLUMNS = [
    "customer_id", "created_at", "region", "segment",
]

SUBSCRIPTIONS_COLUMNS = [
    "subscription_id", "customer_id", "product_id",
    "status", "start_date", "end_date",
]

INVOICES_COLUMNS = [
    "invoice_id", "subscription_id", "amount",
    "currency", "issued_at", "paid_at",
]

DAILY_USAGE_COLUMNS = [
    "subscription_id", "usage_date",
    "requests", "storage_gb", "errors",
]
