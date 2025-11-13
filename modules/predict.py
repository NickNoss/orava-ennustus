import pandas as pd
from .config import PRED_HORIZON_S
from .io_utils import safe_save
from .projection import xy_to_lonlat

def predict_constant_velocity(features_df, horizon_s=PRED_HORIZON_S):
    preds=[]
    for tid, g in features_df.groupby("track_id"):
        g = g.sort_values("timestamp")
        if len(g) < 1:
            continue
        last = g.iloc[-1]
        # last velocity vector
        vx = last["dx"] / last["dt"] if last["dt"] > 0 else 0.0
        vy = last["dy"] / last["dt"] if last["dt"] > 0 else 0.0
        pred_x = last["x"] + vx * horizon_s
        pred_y = last["y"] + vy * horizon_s
        lon,lat = xy_to_lonlat(pred_x, pred_y)
        preds.append({
            "track_id": int(tid),
            "pred_ts": (pd.to_datetime(last["timestamp"]) + pd.to_timedelta(horizon_s, unit="s")).isoformat(),
            "pred_x": pred_x,
            "pred_y": pred_y,
            "pred_lon": lon,
            "pred_lat": lat
        })
    out = pd.DataFrame(preds)
    return out

if __name__ == "__main__":
    feats = pd.read_csv("outputs/track_features.csv", parse_dates=["timestamp"])
    preds = predict_constant_velocity(feats)
    safe_save(preds, "outputs/predictions.csv", index=False)