"""Preparation & delivery: how long orders take, and where the time goes (Q4, Q8, Q9)."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, section


def render() -> None:
    d = data.orders()

    header(
        "Speed",
        "Preparation & delivery",
        "Every order has two clocks: the restaurant's preparation time and the courier's delivery time. Splitting "
        "them shows where to act.",
    )

    g = d.groupby("day_of_the_week")[["food_preparation_time", "delivery_time", "total_time"]].mean().reindex(data.DAYS)
    c = st.columns(4)
    c[0].metric("Average preparation", f"{d['food_preparation_time'].mean():.1f} min", border=True)
    c[1].metric("Average delivery", f"{d['delivery_time'].mean():.1f} min", border=True)
    c[2].metric("Average total", f"{d['total_time'].mean():.1f} min", border=True)
    c[3].metric("Orders over 60 min", f"{(d['total_time'] > 60).mean():.1%}", border=True)

    section("Weekday vs weekend", "Q9. Average minutes per order, split into preparation and delivery.")
    chart(charts.stacked_bars(
        data.DAYS, {"Preparation": g["food_preparation_time"].round(1), "Delivery": g["delivery_time"].round(1)},
        colors=[charts.QUIET, charts.BLUE], hover_fmt=".1f", unit=" min", ytitle="Minutes per order",
    ))
    insight(
        f"Preparation is the same on both ({g['food_preparation_time'].mean():.0f} min). Delivery is "
        f"<b>{g.loc['Weekday', 'delivery_time'] - g.loc['Weekend', 'delivery_time']:.1f} minutes slower on "
        "weekdays</b>, which points to traffic or too few couriers on weekdays, not to the kitchens."
    )

    left, right = st.columns(2, gap="large")
    with left:
        section("Delivery time", "Distribution by day type.")
        chart(charts.histograms(data.by_day(d, "delivery_time"), bin_size=1, start=14.5, xtitle="Delivery minutes",
                                unit=" min"))
        insight("A weekday delivery <b>never takes less than 24 minutes</b> (24-33 min), while weekend deliveries "
                "range from 15 to 30. Fast deliveries only happen at the weekend.")
    with right:
        section("Total time over an hour", "Q8. Share of orders where preparation plus delivery exceeds a limit.")
        limit = st.slider("Limit (minutes)", 40, 65, 60, key="limit")
        share = d.groupby("day_of_the_week")["total_time"].apply(lambda s: (s > limit).mean()).reindex(data.DAYS)
        chart(charts.bars(data.DAYS, share.values, highlight=[True, False], text=[f"{v:.0%}" for v in share.values],
                          hover="%{x}<br><b>%{y:.1%}</b> of orders", ytitle=f"Orders over {limit} min")
              .update_yaxes(tickformat=".0%"))
        insight(f"Overall <b>{(d['total_time'] > limit).mean():.1%}</b> of orders take more than {limit} minutes: "
                f"{share['Weekday']:.0%} on weekdays against {share['Weekend']:.0%} at weekends.")

    section("Preparation time by cuisine", "Do some kitchens take longer?")
    prep = d.groupby("cuisine_type")["food_preparation_time"].agg(["mean", "size"]).sort_values("mean", ascending=False)
    chart(charts.bars(prep.index, prep["mean"].values, horizontal=True, customdata=prep[["size"]].values,
                      hover="<b>%{y}</b><br>%{x:.1f} min on average (%{customdata[0]} orders)",
                      xtitle="Average preparation minutes").update_xaxes(range=[20, 30]))
    insight(f"Every cuisine averages between {prep['mean'].min():.1f} and {prep['mean'].max():.1f} minutes. "
            "Preparation time is not a differentiator; cuisines with few orders (Korean, Vietnamese) look faster "
            "only by chance. The axis starts at 20 minutes to make the small differences visible.")

    section("Do expensive orders take longer?")
    corr = d[["cost_of_the_order", "food_preparation_time", "delivery_time"]].corr()
    names = {"cost_of_the_order": "Order cost", "food_preparation_time": "Preparation time",
             "delivery_time": "Delivery time"}
    chart(charts.heatmap(corr.rename(index=names, columns=names).round(2),
                         hover="%{y} vs %{x}<br>correlation %{z:.2f}", text_fmt=".2f", height=300))
    insight("All correlations are close to 0: price, preparation time and delivery time move independently.")

    footer()
