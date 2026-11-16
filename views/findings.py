"""Landing page: the business questions, the findings and the recommendations."""

import streamlit as st

from lib import data
from lib.ui import cap, finding, footer, header, md


def render() -> None:
    from nav import DELIVERY, DEMAND, METHOD, RATINGS

    m = data.meta()
    d = data.orders()
    wk = (d["day_of_the_week"] == "Weekend").mean()
    per_day = (d["day_of_the_week"] == "Weekend").sum() / 2 / ((d["day_of_the_week"] == "Weekday").sum() / 5)
    dt = d.groupby("day_of_the_week")[["delivery_time", "food_preparation_time"]].mean()
    top4 = d["cuisine_type"].value_counts().head(4)
    big = d["cost_of_the_order"] > 20
    unrated = d["rating"].isna().mean()

    header(
        "Exploratory data analysis · Python, pandas",
        "What drives orders, delivery speed and ratings at FoodHub",
        f"FoodHub connects New York customers with {m['restaurants']} restaurants. I analysed {m['orders']:,} orders "
        "to find out where demand comes from, what slows deliveries down, what customers rate highly and how much "
        "the company earns, so the business can decide where to act first.",
    )

    c = st.columns(4)
    c[0].metric("Orders", f"{m['orders']:,}", border=True)
    c[1].metric("Customers", f"{m['customers']:,}", border=True)
    c[2].metric("Restaurants", m["restaurants"], border=True)
    c[3].metric("FoodHub revenue (commission)", f"${m['commission_total']:,.0f}", border=True)

    st.subheader("Key findings", anchor=False)
    a = st.columns(3)
    finding(
        a[0], f"{wk:.0%}", "of orders are placed at the weekend",
        "Demand is a weekend business",
        f"Per day, a weekend day brings about <b>{per_day:.0f} times</b> as many orders as a weekday.",
        DEMAND, "Orders & cuisines",
    )
    finding(
        a[1], f"+{dt.loc['Weekday', 'delivery_time'] - dt.loc['Weekend', 'delivery_time']:.1f} min",
        "longer delivery on weekdays",
        "Weekday delays happen on the road, not in the kitchen",
        f"Delivery takes {dt.loc['Weekday', 'delivery_time']:.1f} min on weekdays against "
        f"{dt.loc['Weekend', 'delivery_time']:.1f} at weekends, while kitchen time is the same "
        f"(about {dt['food_preparation_time'].mean():.0f} min).",
        DELIVERY, "Preparation & delivery",
    )
    finding(
        a[2], f"{top4.sum() / len(d):.0%}", "of orders come from four cuisines",
        "American, Japanese, Italian and Chinese dominate",
        f"{', '.join(top4.index)}. The top 5 restaurants alone take "
        f"{d['restaurant_name'].value_counts().head(5).sum() / len(d):.0%} of all orders.",
        DEMAND, "Cuisines and restaurants",
    )
    b = st.columns(3)
    finding(
        b[0], f"{big.mean():.0%} → {d.loc[big, 'commission'].sum() / d['commission'].sum():.0%}",
        "orders over $20 → their share of FoodHub's revenue",
        "Larger orders carry the business",
        "The 25% fee on orders over $20 earns more than the 15% fee on everything else combined.",
        RATINGS, "Revenue calculator",
    )
    finding(
        b[1], f"{unrated:.0%}", "of orders are never rated",
        "Ratings are missing, and don't track speed or price",
        "Rated orders score 3 to 5 stars, and the average delivery time and cost are almost identical across those "
        "ratings, so ratings reflect the food more than the service.",
        RATINGS, "Ratings",
    )
    finding(
        b[2], f"{(d['total_time'] > 60).mean():.1%}", "of orders take more than an hour in total",
        "One order in ten is very slow",
        "Preparation plus delivery goes past 60 minutes for about one order in ten, more often on weekdays.",
        DELIVERY, "Total time",
    )

    st.subheader("What I would recommend", anchor=False)
    md(
        "1. **Add delivery capacity on weekdays.** Kitchens are not the bottleneck; "
        "deliveries are.\n"
        "2. **Grow weekday demand with weekday-only offers** on the four big cuisines, where customers already are.\n"
        "3. **Ask for ratings at the right moment** (for example right after delivery, with a small incentive): "
        "four in ten orders give no feedback at all.\n"
        "4. **Protect the top restaurants and larger baskets.** A handful of restaurants and the orders over $20 "
        "carry most of the revenue; promotions (see the eligible restaurants) should keep them on the platform."
    )
    cap("One snapshot of 1,898 orders without dates or locations; recommendations are hypotheses to test.")
    with st.container(border=True):
        md("**How this was done.** The order table was checked, cleaned (unrated orders kept as missing, not zero) "
           "and analysed against the business's questions on demand, speed, ratings and revenue.")
        st.page_link(METHOD, label="Data & method", icon=":material/arrow_forward:")

    footer()
