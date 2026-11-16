"""Loads the prepared data in data/ (built by build_data.py)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data"
DAYS = ["Weekday", "Weekend"]


@st.cache_data
def meta() -> dict:
    return json.loads((DATA / "meta.json").read_text(encoding="utf-8"))


@st.cache_data
def table(name: str) -> pd.DataFrame:
    return pd.read_parquet(DATA / f"{name}.parquet")


@st.cache_data
def orders() -> pd.DataFrame:
    return table("orders")


def commission(cost: pd.Series, high: float, low: float, high_from: float, low_from: float) -> pd.Series:
    return cost * np.where(cost > high_from, high, np.where(cost > low_from, low, 0.0))


def by_day(df: pd.DataFrame, col: str) -> dict[str, pd.Series]:
    return {d: df.loc[df["day_of_the_week"] == d, col] for d in DAYS}
