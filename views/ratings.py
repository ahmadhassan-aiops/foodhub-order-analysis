"""Ratings, the promotion rule, and FoodHub's commission revenue (Q3, Q6, Q7)."""

import streamlit as st

from lib import charts, data
from lib.ui import cap, chart, footer, header, insight, section


def render() -> None:
    d = data.orders()

    header(
        "Customers & money",
        "Ratings, promotions & revenue",
        "What customers rate, which restaurants qualify for the promotion, and how much FoodHub earns from its "
        "commission. The rules are adjustable so you can test alternatives.",
    )

    section("Ratings", "Share of orders by rating.")
    r = d["rating"].map(lambda v: "Not rated" if v != v else f"{int(v)} stars").value_counts()
    r = r.reindex(["Not rated", "3 stars", "4 stars", "5 stars"])
    left, right = st.columns(2, gap="large")
    with left:
        chart(charts.bars(r.index, (r / len(d)).values, highlight=[True, False, False, False],
                          text=[f"{v / len(d):.0%}" for v in r.values], customdata=r.values[:, None],
                          hover="%{x}<br><b>%{y:.0%}</b> (%{customdata[0]:,} orders)").update_yaxes(tickformat=".0%"))
    with right:
        by = d.dropna(subset=["rating"]).groupby("rating")[["delivery_time", "cost_of_the_order"]].mean()
        st.dataframe(
            by.rename(index=lambda v: f"{int(v)} stars").rename(columns={"delivery_time": "Avg delivery (min)",
                                                                          "cost_of_the_order": "Avg cost ($)"}),
            column_config={"Avg delivery (min)": st.column_config.NumberColumn(format="%.1f"),
                           "Avg cost ($)": st.column_config.NumberColumn(format="$%.2f")},
        )
    insight(f"<b>{r['Not rated'] / len(d):.0%} of orders have no rating.</b> No order is rated below 3 stars, and "
            "3-, 4- and 5-star orders have nearly the same delivery time and cost, so ratings say little about "
            "speed or price.")

    section("Promotion eligibility", "Q6. Restaurants with more than N ratings and an average above X qualify.")
    a, b = st.columns(2)
    min_n = a.slider("Minimum number of ratings", 10, 100, 50, key="min_n")
    min_avg = b.slider("Minimum average rating", 3.5, 4.8, 4.0, step=0.1, key="min_avg")
    rs = d.dropna(subset=["rating"]).groupby("restaurant_name")["rating"].agg(count="count", average="mean")
    ok = rs[(rs["count"] > min_n) & (rs["average"] > min_avg)].sort_values("average", ascending=False)
    st.dataframe(ok.reset_index().rename(columns={"restaurant_name": "Restaurant", "count": "Ratings",
                                                  "average": "Average rating"}),
                 hide_index=True, column_config={"Average rating": st.column_config.NumberColumn(format="%.2f")})
    cap(f"{len(ok)} restaurants qualify. With the original rule (more than 50 ratings, average above 4) these are "
        "Blue Ribbon Fried Chicken, Blue Ribbon Sushi, Shake Shack and The Meatball Shop.")
    insight("Only the very busiest restaurants can reach 50 ratings, because so many orders go unrated. More "
            "ratings would let smaller, well-liked restaurants qualify too.")

    section("FoodHub's revenue", "Q7. FoodHub charges restaurants a commission on each order.")
    a, b, c, e = st.columns(4)
    high = a.number_input("Rate on large orders (%)", 0, 50, 25, key="high") / 100
    high_from = b.number_input("Large order: over ($)", 5, 50, 20, key="high_from")
    low = c.number_input("Rate on other orders (%)", 0, 50, 15, key="low") / 100
    low_from = e.number_input("No fee at or below ($)", 0, 20, 5, key="low_from")
    fee = data.commission(d["cost_of_the_order"], high, low, high_from, low_from)
    big = d["cost_of_the_order"] > high_from
    k = st.columns(3)
    k[0].metric("Commission revenue", f"${fee.sum():,.2f}", border=True,
                delta=f"{fee.sum() - data.meta()['commission_total']:+,.0f} vs current rules" if abs(fee.sum() - data.meta()['commission_total']) > 0.5 else None)
    k[1].metric(f"Orders over ${high_from}", f"{big.mean():.0%}", border=True)
    k[2].metric("Their share of revenue", f"{fee[big].sum() / fee.sum():.0%}" if fee.sum() else "n/a", border=True)
    chart(charts.histograms({"Order cost": d["cost_of_the_order"]}, bin_size=1, start=0, xtitle="Order cost ($)",
                            percent=False).update_traces(marker_color=charts.BLUE)
          .add_vline(x=high_from, line=dict(color=charts.INK_2, dash="dot", width=1.5)))
    insight(f"With the current rules FoodHub earns <b>${data.meta()['commission_total']:,.2f}</b>. Order costs "
            "peak around $12 and again around $24 and $29. Moving the large-order threshold even a few dollars shifts many "
            "orders between the two rates, so it is the most sensitive lever.")

    footer()
