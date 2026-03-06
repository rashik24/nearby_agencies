import numpy as np
from sklearn.neighbors import BallTree

EARTH_RADIUS_MILES = 3958.8


def build_tree(df):

    coords = df[["Latitude","Longitude"]].astype(float).to_numpy()
    coords = np.radians(coords)

    tree = BallTree(coords, metric="haversine")

    return tree


def find_nearby(tree, df, agency_name, radius_miles=10):

    coords = df[["Latitude","Longitude"]].astype(float).to_numpy()
    coords_rad = np.radians(coords)

    idx = df[df["Agency"] == agency_name].index[0]

    point = coords_rad[idx].reshape(1,-1)

    radius = radius_miles / EARTH_RADIUS_MILES

    dist, ind = tree.query_radius(point, r=radius, return_distance=True)

    ind = ind[0]
    dist = dist[0] * EARTH_RADIUS_MILES

    nearby = df.iloc[ind].copy()

    nearby["distance_miles"] = dist

    return nearby.sort_values("distance_miles")
