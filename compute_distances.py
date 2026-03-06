import pandas as pd
from math import radians, sin, cos, sqrt, atan2

def haversine_miles(lat1, lon1, lat2, lon2):

    R = 3958.8

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


df = pd.read_csv("fbcenc_hours.csv")

ag = df[["Agency","Latitude","Longitude"]].drop_duplicates().reset_index(drop=True)

dist_rows = []

for i in range(len(ag)):
    for j in range(i+1, len(ag)):

        A = ag.loc[i,"Agency"]
        B = ag.loc[j,"Agency"]

        lat1 = ag.loc[i,"Latitude"]
        lon1 = ag.loc[i,"Longitude"]

        lat2 = ag.loc[j,"Latitude"]
        lon2 = ag.loc[j,"Longitude"]

        d = haversine_miles(lat1, lon1, lat2, lon2)

        dist_rows.append((A,B,d))
        dist_rows.append((B,A,d))


dist_df = pd.DataFrame(
    dist_rows,
    columns=["agency_1","agency_2","distance_miles"]
)

dist_df.to_csv("agency_distances.csv", index=False)

print("Distance matrix saved.")
