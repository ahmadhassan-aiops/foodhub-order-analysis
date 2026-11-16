"""
FoodHub: what drives orders, delivery speed and ratings for a New York food delivery app.
An interactive presentation of Ahmad Hassan's analysis. All data ships with the app.
"""

import streamlit as st

st.set_page_config(
    page_title="FoodHub orders | Ahmad Hassan",
    page_icon=":material/delivery_dining:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from lib.ui import inject_css  # noqa: E402
from nav import PAGES  # noqa: E402

inject_css()
st.navigation(PAGES, position="top").run()
