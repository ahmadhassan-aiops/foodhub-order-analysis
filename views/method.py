"""Data & method: the order table, cleaning decisions, the business questions, limits."""

import pandas as pd
import streamlit as st

from lib import data
from lib.site import NOTEBOOK_URL
from lib.ui import footer, header, md, section


def render() -> None:
    m = data.meta()

    header(
        "Data & method",
        "How the analysis was done",
        "The data, the cleaning decisions, the business questions and the limits of the study. The full Python "
        f'work is in the <a href="{NOTEBOOK_URL}" target="_blank">notebook</a>.',
    )

    section("The data")
    md(f"One table of **{m['orders']:,} orders** ({m['raw_shape'][1]} columns) from FoodHub, a fictional New York "
       "food delivery aggregator used as a training case. Customer IDs are anonymised numbers.")
    st.table(pd.DataFrame([
        ("order_id, customer_id", "Unique order and (anonymised) customer identifiers"),
        ("restaurant_name, cuisine_type", "Where the order was placed and the type of food"),
        ("cost_of_the_order", "Order value in dollars"),
        ("day_of_the_week", "Weekday (Monday to Friday) or Weekend (Saturday, Sunday)"),
        ("rating", "1 to 5 stars, or \"Not given\""),
        ("food_preparation_time", "Minutes from the restaurant confirming the order to the food being ready"),
        ("delivery_time", "Minutes from pickup to delivery"),
    ], columns=["Column", "Meaning"]), hide_index=True, border="horizontal")
    with st.expander("Look at the raw data (50 random orders)"):
        st.dataframe(data.table("sample_orders"), hide_index=True, height=320)

    section("Cleaning decisions")
    st.table(pd.DataFrame([
        ("Missing values", f"{m['missing']} empty cells, {m['duplicates']} duplicate rows", "Nothing to fix"),
        ("Ratings", f"{m['not_given']:,} orders rated \"Not given\" (text in a number column)",
         "Turned into missing values, not zero, so they don't drag averages down"),
        ("Total time", "Not in the data", "Added as preparation time + delivery time"),
        ("Commission", "Not in the data", "Added: 25% of orders over $20, 15% of orders over $5, 0 otherwise"),
    ], columns=["Item", "What was found", "How it was handled"]), hide_index=True, border="horizontal")

    section("The business questions")
    st.table(pd.DataFrame([
        ("Q1", "Top 5 restaurants by number of orders", "Orders & cuisines"),
        ("Q2", "Most popular cuisine at the weekend", "Orders & cuisines (American)"),
        ("Q3", "Share of orders costing more than $20", "Ratings, promotions & revenue"),
        ("Q4", "Mean delivery time", "Preparation & delivery"),
        ("Q5", "Top 3 customers for a 20% voucher", "Orders & cuisines"),
        ("Q6", "Restaurants eligible for the promotion", "Ratings, promotions & revenue"),
        ("Q7", "FoodHub's commission revenue", "Ratings, promotions & revenue"),
        ("Q8", "Share of orders taking over 60 minutes in total", "Preparation & delivery"),
        ("Q9", "Delivery time on weekdays vs weekends", "Preparation & delivery"),
    ], columns=["#", "Question", "Answered on"]).map(lambda v: v.replace("$", r"\$") if isinstance(v, str) else v),
        hide_index=True, border="horizontal")

    section("Limits of this data")
    md("- **One snapshot, no dates or times.** Weekday vs weekend is the only time information; lunch vs dinner "
       "or seasonal effects can't be studied.\n"
       "- **No locations.** Delivery distance, which surely affects delivery time, is unknown.\n"
       "- **Ratings are self-selected.** Customers who rate may differ from those who don't.\n"
       "- **Descriptive, not causal.** The recommendations are hypotheses to test.")

    section("How this app is built")
    md("Python, pandas and Plotly in a Streamlit app. `build_data.py` cleans the CSV once and saves it as a "
       f"Parquet file that ships with the app. Data built on {m['built']}.")

    footer()
