"""Page registry, shared by app.py and pages that link to other pages."""

import streamlit as st

from views import delivery, demand, findings, method, ratings

FINDINGS = st.Page(findings.render, title="Key findings", icon=":material/insights:", url_path="findings", default=True)
DEMAND = st.Page(demand.render, title="Orders & cuisines", icon=":material/restaurant:", url_path="orders")
DELIVERY = st.Page(delivery.render, title="Preparation & delivery", icon=":material/schedule:", url_path="delivery")
RATINGS = st.Page(ratings.render, title="Ratings, promotions & revenue", icon=":material/star:", url_path="ratings")
METHOD = st.Page(method.render, title="Data & method", icon=":material/dataset:", url_path="method")

PAGES = [FINDINGS, DEMAND, DELIVERY, RATINGS, METHOD]
