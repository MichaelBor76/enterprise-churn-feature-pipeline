import os
import yaml
import pandas as pd
from pathlib import Path

def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def write_parquet(df: pd.DataFrame, path: str) -> None:
    ensure_dir(os.path.dirname(path))
    df.to_parquet(path, index=False)
