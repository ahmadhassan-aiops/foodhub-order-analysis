"""Orders & cuisines: when customers order, what they order, from where, and who orders most."""

import streamlit as st

from lib import charts, data
from lib.ui import chart, footer, header, insight, section


def render() -> None:
    d = data.orders()

    header(
        "Demand",
        "Orders & cuisines",
        "Where FoodHub's orders come from: the day of the week, the cuisine, the restaurant and the customer.",
    )

    left, right = st.columns(2, gap="large")
    with left:
        section("Weekday vs weekend", "Orders in total, and per day (the weekend has 2 days, the week 5).")
        n = d["day_of_the_week"].value_counts().reindex(data.DAYS)
        per_day = n / [5, 2]
        mode = st.segmented_control("Show", ["Per day", "In total"], default="Per day", key="perday",
                                    label_visibility="collapsed") or "Per day"
        v = per_day if mode == "Per day" else n
        chart(charts.bars(data.DAYS, v.values, highlight=[False, True], text=[f"{x:,.0f}" for x in v.values],
                          hover="%{x}<br><b>%{y:,.0f} orders</b>", ytitle="Orders per day" if mode == "Per day" else "Orders"))
        insight(f"The weekend has <b>{n['Weekend']:,}</b> orders against {n['Weekday']:,} on weekdays. Per day "
                f"that is about <b>{per_day['Weekend']:.0f}</b> against {per_day['Weekday']:.0f}.")
    with right:
        section("Cuisines", "Orders by cuisine type.")
        cu = d["cuisine_type"].value_counts()
        chart(charts.bars(cu.index, cu.values, horizontal=True, highlight=[i < 4 for i in range(len(cu))],
                          customdata=(cu / len(d)).values[:, None],
                          hover="<b>%{y}</b><br>%{x:,} orders (%{customdata[0]:.0%})"))
        insight(f"The top four cuisines (highlighted) take <b>{cu.head(4).sum() / len(d):.0%}</b> of orders. "
                "The other ten share what is left.")

    section("Cuisine by day", "Does the cuisine mix change at the weekend? Share of each day's orders.")
    mix = (d.groupby("day_of_the_week")["cuisine_type"].value_counts(normalize=True).unstack(0).reindex(cu.index[:8]))
    chart(charts.grouped_bars(mix.index, {k: mix[k].values for k in data.DAYS}, hover_fmt=".1%",
                              ytitle="Share of the day's orders").update_yaxes(tickformat=".0%"))
    insight("The mix is <b>almost the same</b> on weekdays and at the weekend: the weekend brings more orders, not "
            "different tastes.")

    section("Restaurants", "Q1. The busiest restaurants by number of orders.")
    k = st.slider("Restaurants to show", 5, 25, 10, key="nrest")
    r = d.groupby("restaurant_name").agg(orders=("order_id", "size"), revenue=("cost_of_the_order", "sum"),
                                         cuisine=("cuisine_type", "first")).sort_values("orders", ascending=False)
    top = r.head(k)
    chart(charts.bars(top.index, top["orders"].values, horizontal=True, customdata=top[["cuisine", "revenue"]].values,
                      hover="<b>%{y}</b> (%{customdata[0]})<br>%{x} orders · $%{customdata[1]:,.0f} of food sold"))
    insight(f"Of {len(r)} restaurants, the top 5 take <b>{r['orders'].head(5).sum() / len(d):.0%}</b> of orders and "
            f"the top 10% ({len(r) // 10}) take {r['orders'].head(len(r) // 10).sum() / len(d):.0%}. Shake Shack "
            "alone has more orders than most cuisines.")

    section("Customers", "How often customers order. Q5: the three most frequent customers get a 20% voucher.")
    vc = d["customer_id"].value_counts()
    freq = vc.value_counts().sort_index()
    left, right = st.columns([2, 1], gap="large")
    with left:
        chart(charts.bars([str(i) for i in freq.index], freq.values, highlight=[i == 1 for i in freq.index],
                          hover="%{x} orders<br><b>%{y:,} customers</b>", xtitle="Orders per customer", ytitle="Customers"))
    with right:
        st.dataframe(vc.head(3).rename_axis("Customer ID").reset_index(name="Orders"), hide_index=True)
        st.caption("Voucher winners (customer IDs are anonymised).")
    insight(f"<b>{(vc == 1).mean():.0%}</b> of customers ordered only once in this snapshot; "
            f"{(vc > 1).mean():.0%} came back at least once.")

    footer()
