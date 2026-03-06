import numpy as np
from sklearn.neighbors import BallTree


def build_tree(df):

    coords = np.radians(df[["Latitude", "Longitude"]].values)

    tree = BallTree(coords, metric="haversine")

    return tree


def find_nearby(tree, df, agency_name, radius_miles=10):

    earth_radius = 3958.8

    idx = df[df["Agency"] == agency_name].index[0]

    point = df.loc[idx, ["Latitude", "Longitude"]].astype(float).to_numpy().reshape(1, -1)

    point = np.radians(point)

    radius = radius_miles / earth_radius

    ind = tree.query_radius(point, r=radius)[0]

    nearby = df.iloc[ind].copy()

    return nearby
