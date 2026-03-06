import streamlit as st
import pandas as pd
from datetime import datetime
from distance_utils import build_tree, find_nearby


# ----------------------------
# Load dataset (cached)
# ----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("fbcenc_hourly.csv")
    return df

df = load_data()


# ----------------------------
# Unique agencies
# ----------------------------

ag = df[["Agency","Latitude","Longitude"]].drop_duplicates()

ag["Latitude"] = ag["Latitude"].astype(float)
ag["Longitude"] = ag["Longitude"].astype(float)

ag = ag.dropna(subset=["Latitude","Longitude"])


# ----------------------------
# Build spatial index (cached)
# ----------------------------

@st.cache_resource
def get_tree(data):
    return build_tree(data)

tree = get_tree(ag)


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


# ----------------------------
# Find nearby agencies
# ----------------------------

nearby = find_nearby(tree, ag, agency_selected, radius)


# ----------------------------
# Find agencies open now
# ----------------------------

now = datetime.now()

week = (now.day - 1)//7 + 1
day = now.strftime("%A")
hour = now.hour

open_now = df[
    (df["Week"] == week) &
    (df["Day"] == day) &
    (df["Hour"] == hour)
]


# ----------------------------
# Filter nearby agencies by open status
# ----------------------------

nearby = nearby[nearby["Agency"].isin(open_now["Agency"])]


# ----------------------------
# Display results
# ----------------------------

st.subheader("Nearby Agencies Open Now")

st.dataframe(nearby)

st.map(nearby[["Latitude","Longitude"]])
