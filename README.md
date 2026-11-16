# What drives orders, delivery speed and ratings at FoodHub

An interactive presentation of an exploratory data analysis by **Ahmad Hassan** (AI Engineer).
FoodHub is a New York food delivery aggregator. The analysis of 1,898 orders answers the business's questions on
demand, delivery speed, ratings and commission revenue.

- **Key findings**: six results and four recommendations.
- **Orders & cuisines**: weekday vs weekend demand, cuisines, top restaurants, repeat customers.
- **Preparation & delivery**: where the time goes, weekday vs weekend, orders over an hour.
- **Ratings, promotions & revenue**: ratings, an adjustable promotion rule and a commission calculator.
- **Data & method**: cleaning decisions, the nine business questions, limits.

Original notebook: [AIOPS-Portfolio-Projects / Online Restaurant Data Analysis](https://github.com/ahmadhassan-aiops/AIOPS-Portfolio-Projects/tree/main/1.%20Data-analysis-with-python-Projects/Online%20Restaurant%20Data%20Analysis)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the data: `python build_data.py "path/to/Online Restaurant Data Analysis"` (folder with `foodhub_order.csv`).

Structure: `app.py` (entry), `nav.py` (pages), `views/` (one module per page), `lib/` (data loading, charts, UI),
`build_data.py` (CSV to Parquet), `data/` (prepared data shipped with the app), `Dockerfile` (port 7860).

## Data

A training dataset of a fictional company with anonymised customer IDs.
