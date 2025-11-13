import folium
import pandas as pd
from .projection import xy_to_lonlat

def visualize(track_points_csv="outputs/track_points.csv",
              predictions_csv="outputs/predictions.csv",
              out_html="outputs/map_predictions.html"):
    tp = pd.read_csv(track_points_csv, parse_dates=["timestamp"])
    preds = pd.read_csv(predictions_csv)
    # center map
    center_lat = tp["latitude"].mean() if "latitude" in tp.columns else preds["pred_lat"].mean()
    center_lon = tp["longitude"].mean() if "longitude" in tp.columns else preds["pred_lon"].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    for tid, g in tp.groupby("track_id"):
        coords = list(zip(g["latitude"], g["longitude"]))
        folium.PolyLine(coords, color="blue", weight=2).add_to(m)
        # last point
        last = coords[-1]
        folium.CircleMarker(location=last, radius=3, color="black").add_to(m)

    for _, r in preds.iterrows():
        folium.Marker([r["pred_lat"], r["pred_lon"]], icon=folium.Icon(color="red"), popup=f"pred {int(r['track_id'])}").add_to(m)

    m.save(out_html)
    print(f"Saved map to {out_html}")

if __name__ == "__main__":
    visualize()