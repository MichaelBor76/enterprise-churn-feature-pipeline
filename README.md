# enterprise-churn-feature-pipeline

# Enterprise Churn Feature Pipeline

This project demonstrates an end‑to‑end **ELT pipeline** for an enterprise‑style
**churn prediction** use case. It ingests synthetic data from multiple systems
(CRM, billing, and usage), loads it into a local environment, and builds
**ML‑ready feature tables** for model training.

The focus is on:
- realistic **enterprise data modeling**
- **feature engineering** for structured/tabular ML
- clear, reproducible **data pipeline structure**

---

## 🏗️ Architecture

**Sources (synthetic):**
- `CRM` – customers, subscriptions, products
- `Billing` – invoices, payments, renewals
- `Usage` – daily usage metrics per subscription

**Pipeline stages:**
1. **Ingest**  
   - Read CSV/JSON from `data/raw/`
   - Apply basic schema validation
   - Write normalized tables to `data/processed/`

2. **Transform (ELT)**  
   - Use Python + pandas to:
     - join CRM, billing, and usage
     - compute 30‑day / 90‑day aggregates
     - build churn‑relevant features (recency, frequency, monetary, incidents)
   - Write final feature table to `data/features/churn_features.parquet`

3. **Explore**  
   - Use `notebooks/01_exploration.ipynb` to:
     - inspect distributions
     - check missingness
     - verify label/feature consistency

---

## 🧩 Data Model (Simplified)

### CRM
- `customers`  
  - `customer_id`, `created_at`, `region`, `segment`
- `subscriptions`  
  - `subscription_id`, `customer_id`, `product_id`, `status`, `start_date`, `end_date`
- `products`  
  - `product_id`, `name`, `plan_tier`

### Billing
- `invoices`  
  - `invoice_id`, `subscription_id`, `amount`, `currency`, `issued_at`, `paid_at`
- `payments`  
  - `payment_id`, `invoice_id`, `status`, `paid_at`

### Usage
- `daily_usage`  
  - `subscription_id`, `usage_date`, `requests`, `storage_gb`, `errors`

### Target
- `churn_label` (derived)  
  - `is_churned` (1/0) based on subscription status and end_date

---

## 🔧 Tech Stack

- **Python** 3.10+
- **pandas** for transformations
- **pyarrow** / **fastparquet** for Parquet
- **Jupyter** for exploration

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/enterprise-churn-feature-pipeline.git
cd enterprise-churn-feature-pipeline

### 2. Install dependencies

```bash

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

### 3. Configure

Copy the example config:

```bash

cp config/config.example.yaml config/config.yaml

Edit config/config.yaml to adjust paths if needed.

### 4. Run ingestion

```bash

python -m src.ingest_crm
python -m src.ingest_billing
python -m src.ingest_usage

This will read synthetic raw data from data/raw/ and write normalized tables
to data/processed/.

### 5. Run feature transformation

```bash

python -m src.transform_features

This will create data/features/churn_features.parquet.

### 6. Explore in notebook

```bash

jupyter notebook notebooks/01_exploration.ipynb
