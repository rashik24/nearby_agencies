import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ----------------------------
# Load data
# ----------------------------

@st.cache_data
def load_hours():
    return pd.read_csv("fbcenc_hourly.csv")

@st.cache_data
def load_distances():
    df = pd.read_csv("agency_distances.csv")

    # If columns are unnamed (0,1,2) fix them
    if list(df.columns) != ["agency_1", "agency_2", "distance_miles"]:
        df.columns = ["agency_1", "agency_2", "distance_miles"]

    return df


df = load_hours()
distances = load_distances()
# ----------------------------
# Unique agencies
# ----------------------------

ag = df[["Agency", "Latitude", "Longitude"]].drop_duplicates().reset_index(drop=True)

ag["Latitude"] = pd.to_numeric(ag["Latitude"], errors="coerce")
ag["Longitude"] = pd.to_numeric(ag["Longitude"], errors="coerce")
ag = ag.dropna(subset=["Latitude", "Longitude"])

# ----------------------------
# UI
# ----------------------------

st.title("Food Pantry Finder")

agency_selected = st.selectbox(
    "Select Agency",
    sorted(ag["Agency"].unique())
)

radius = st.slider(
    "Search radius (miles)",
    1,
    50,
    10
)

show_only_open = st.checkbox("Show only agencies open now", value=True)

# ----------------------------
# Filter nearby agencies from precomputed distances
# ----------------------------

nearby = distances[
    (distances["agency_1"] == agency_selected) &
    (distances["distance_miles"] <= radius)
].copy()

nearby["distance_miles"] = nearby["distance_miles"].round(2)
nearby = (
    nearby.groupby("agency_2", as_index=False)
    .agg({"distance_miles": "min"})
)
# join coordinates if you need them later
nearby = nearby.merge(
    ag,
    left_on="agency_2",
    right_on="Agency",
    how="left"
)

# remove the selected agency if it exists in file
nearby = nearby[nearby["Agency"] != agency_selected]

# ----------------------------
# Find agencies open now
# ----------------------------

now = datetime.now()
week = (now.day - 1) // 7 + 1
day = now.strftime("%A")
hour = now.hour

open_now = df[
    (df["Week"] == week) &
    (df["Day"] == day) &
    (df["Hour"] == hour)
]

if show_only_open:
    nearby = nearby[nearby["Agency"].isin(open_now["Agency"])]

# ----------------------------
# Display results
# ----------------------------

st.subheader("Nearby Agencies")

st.dataframe(
    nearby[["Agency", "distance_miles"]]
    .rename(columns={"Agency": "Nearby Agency"})
)
