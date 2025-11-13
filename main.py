import os
import pandas as pd
from config import DETECTIONS_CSV, TRACK_POINTS_CSV, TRACK_FEATURES_CSV, PREDICTIONS_CSV, MAP_HTML
from modules.io_utils import read_detections, safe_save
from modules.linking import link_tracks
from modules.features import compute_features
from modules.predict import predict_constant_velocity
from modules.visualize import visualize

def main():
    print("Ladataan havaintodata...")
    detections = read_detections()
    print(f"Ladattu {len(detections)} havaintoa.")

    print("Linkitetään havainnot yksittäisiin jälkiin...")
    track_points = link_tracks(detections)
    safe_save(track_points, TRACK_POINTS_CSV, index=False)

    print("Lasketaan piirteet (nopeus, suunta jne.)...")
    features = compute_features(track_points)
    safe_save(features, TRACK_FEATURES_CSV, index=False)

    print("Ennustetaan tuleva sijainti (30 min eteenpäin)...")
    predictions = predict_constant_velocity(features)
    safe_save(predictions, PREDICTIONS_CSV, index=False)

    print("Luodaan visualisointi...")
    visualize(TRACK_POINTS_CSV, PREDICTIONS_CSV, MAP_HTML)

    print(f"Valmis! Avaa {MAP_HTML} selaimessa.")

if __name__ == "__main__":
    main()
