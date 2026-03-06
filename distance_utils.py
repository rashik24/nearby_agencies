import numpy as np
from sklearn.neighbors import BallTree

EARTH_RADIUS_MILES = 3958.8


def build_tree(df):

    coords = df[["Latitude", "Longitude"]].astype(float).to_numpy()

    # convert to radians
    coords_rad = np.radians(coords)

    tree = BallTree(coords_rad, metric="haversine")

    return tree, coords_rad


def find_nearby(tree, coords_rad, df, agency_name, radius_miles=10):

    idx = df.index[df["Agency"] == agency_name][0]

    point = coords_rad[idx].reshape(1, -1)

    radius = radius_miles / EARTH_RADIUS_MILES

    dist, ind = tree.query_radius(point, r=radius, return_distance=True)

    ind = ind[0]
    dist = dist[0] * EARTH_RADIUS_MILES  # convert radians → miles

    nearby = df.iloc[ind].copy()

    nearby["distance_miles"] = dist

    nearby = nearby.sort_values("distance_miles")

    return nearby
