import pandas as pd
import numpy as np
from math import atan2, degrees
from .io_utils import safe_save

def compute_features(track_points_df):
    df = track_points_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["track_id","timestamp"])
    df["dt"] = df.groupby("track_id")["timestamp"].diff().dt.total_seconds().fillna(0)
    df["dx"] = df.groupby("track_id")["x"].diff().fillna(0)
    df["dy"] = df.groupby("track_id")["y"].diff().fillna(0)
    df["distance"] = np.hypot(df["dx"], df["dy"])
    df["speed"] = df["distance"] / df["dt"].replace(0, np.nan)
    def _bearing(row):
        if row["distance"] == 0 or np.isnan(row["distance"]):
            return 0.0
        return degrees(atan2(row["dy"], row["dx"]))
    df["bearing"] = df.apply(_bearing, axis=1)
    df = df.fillna(0)
    return df

if __name__ == "__main__":
    import os
    tp = pd.read_csv("outputs/track_points.csv", parse_dates=["timestamp"])
    feats = compute_features(tp)
    safe_save(feats, "outputs/track_features.csv", index=False)