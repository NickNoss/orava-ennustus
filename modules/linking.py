import numpy as np
import pandas as pd
from .projection import lonlat_to_xy
from .io_utils import safe_save
from config import LINK_MAX_DIST_M, LINK_MAX_DT_S

def link_tracks(df):
    df = df.sort_values("timestamp").reset_index(drop=True).copy()
    xs, ys = zip(*[lonlat_to_xy(lon,lat) for lon,lat in zip(df["longitude"], df["latitude"])])
    df["x"] = xs; df["y"] = ys

    tracks = []
    current_track = [0]
    for i in range(1, len(df)):
        dt = (df.loc[i,"timestamp"] - df.loc[i-1,"timestamp"]).total_seconds()
        dist = np.hypot(df.loc[i,"x"]-df.loc[i-1,"x"], df.loc[i,"y"]-df.loc[i-1,"y"])
        if dt <= LINK_MAX_DT_S and dist <= LINK_MAX_DIST_M and df.loc[i,"species"] == df.loc[i-1,"species"]:
            current_track.append(i)
        else:
            tracks.append(current_track)
            current_track = [i]
    if current_track:
        tracks.append(current_track)

    rows=[]
    for tid, idxs in enumerate(tracks):
        for idx in idxs:
            r = df.loc[idx].to_dict()
            r["track_id"] = int(tid)
            rows.append(r)
    out = pd.DataFrame(rows)
    return out

if __name__ == "__main__":
    import sys
    from .io_utils import read_detections
    df = read_detections()
    tp = link_tracks(df)
    safe_save(tp, "outputs/track_points.csv", index=False)