import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
DETECTIONS_CSV = os.path.join(DATA_DIR, 'detections.csv')

OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
TRACK_POINTS_CSV = os.path.join(OUTPUT_DIR, 'track_points.csv')
TRACK_FEATURES_CSV = os.path.join(OUTPUT_DIR, 'track_features.csv')
PREDICTIONS_CSV = os.path.join(OUTPUT_DIR, 'predictions.csv')
MAP_HTML = os.path.join(OUTPUT_DIR, 'map.html')

# thresholds for linking (meters, seconds)
LINK_MAX_DIST_M = 1500
LINK_MAX_DT_S = 2 * 3600  # 2 hours

# prediction horizon (seconds)
PRED_HORIZON_S = 30 * 60  # 30 min