import pandas as pd
from config import DETECTIONS_CSV

def read_detections(path=None):
    path = path or DETECTIONS_CSV
    df = pd.read_csv(path, parse_dates=['timestamp'])
    # required columns: image_path,timestamp,species,confidence,latitude,longitude,bbox (bbox optional)
    expected = {"image_path","timestamp","species","confidence","latitude","longitude"}
    if not expected.issubset(set(df.columns)):
        raise ValueError(f"detections CSV must contain columns: {expected}")
    return df

def safe_save(df, path, index=False):
    df.to_csv(path, index=index)
    print(f"Saved to {path}")