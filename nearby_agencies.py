from datetime import datetime

def get_open_agencies(df):

    now=datetime.now()

    week=(now.day-1)//7 + 1
    day=now.strftime("%A")
    hour=now.hour

    open_now=df[
        (df["Week"]==week) &
        (df["Day"]==day) &
        (df["Hour"]==hour)
    ]

    return open_now
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

df = pd.read_csv("/Users/rsiddiq2/Downloads/llama-index/fbcenc_hourly.csv")

# keep unique agency locations
agencies = df[["Agency","Latitude","Longitude"]].drop_duplicates()

from datetime import datetime

def get_open_agencies(df):

    now=datetime.now()

    week=(now.day-1)//7 + 1
    day=now.strftime("%A")
    hour=now.hour

    open_now=df[
        (df["Week"]==week) &
        (df["Day"]==day) &
        (df["Hour"]==hour)
    ]

    return open_now

import streamlit as st
import pandas as pd
from datetime import datetime

df = pd.read_csv("/Users/rsiddiq2/Downloads/llama-index/fbcenc_hourly.csv")
distances=pd.read_csv("agency_distances.csv")

st.title("Food Pantry Finder")

agency_selected=st.selectbox(
    "Select Agency",
    df["Agency"].unique()
)

max_distance=st.slider(
    "Max Distance (km)",
    1,
    50,
    10
)

# ---------------------
# get open agencies
# ---------------------

now=datetime.now()
week=(now.day-1)//7 + 1
day=now.strftime("%A")
hour=now.hour

open_now=df[
    (df["Week"]==week) &
    (df["Day"]==day) &
    (df["Hour"]==hour)
]

open_agencies=open_now["Agency"].unique()

# ---------------------
# distance filter
# ---------------------

nearby=distances[
    (distances["agency_1"]==agency_selected) &
    (distances["distance_km"]<=max_distance)
]

nearby=nearby[nearby["agency_2"].isin(open_agencies)]

nearby=nearby.merge(
    df[["Agency","Latitude","Longitude"]].drop_duplicates(),
    left_on="agency_2",
    right_on="Agency"
)

st.write("Open Nearby Agencies")

st.dataframe(
    nearby[["Agency","distance_km","Latitude","Longitude"]]
)

st.map(nearby[["Latitude","Longitude"]])