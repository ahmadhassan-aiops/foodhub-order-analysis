"""
Offline build step: foodhub_order.csv -> data/orders.parquet + data/meta.json.

    python build_data.py "W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Online Restaurant Data Analysis"

Cleaning: "Not given" ratings become missing (not zero); total time = preparation + delivery.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_RAW = Path("W:/Portfolio Projects/1. Data-analysis-with-python-Projects/Online Restaurant Data Analysis")
OUT = Path(__file__).parent / "data"


def commission(cost: pd.Series, high: float = 0.25, low: float = 0.15, high_from: float = 20, low_from: float = 5) -> pd.Series:
    """FoodHub's fee to restaurants: 25% on orders over $20, 15% on orders over $5, nothing below."""
    return cost * np.where(cost > high_from, high, np.where(cost > low_from, low, 0.0))


def main(raw: Path) -> None:
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(raw / "foodhub_order.csv")
    raw_shape = list(df.shape)
    df.sample(50, random_state=7).to_parquet(OUT / "sample_orders.parquet", index=False)

    not_given = int((df["rating"] == "Not given").sum())
    df["rating"] = pd.to_numeric(df["rating"].replace("Not given", np.nan))
    df["total_time"] = df["food_preparation_time"] + df["delivery_time"]
    df["commission"] = commission(df["cost_of_the_order"])
    df.to_parquet(OUT / "orders.parquet", index=False)

    meta = {
        "built": date.today().isoformat(),
        "raw_shape": raw_shape,
        "orders": int(len(df)),
        "customers": int(df["customer_id"].nunique()),
        "restaurants": int(df["restaurant_name"].nunique()),
        "cuisines": int(df["cuisine_type"].nunique()),
        "not_given": not_given,
        "missing": int(df.drop(columns="rating").isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "commission_total": float(df["commission"].sum()),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_RAW)
