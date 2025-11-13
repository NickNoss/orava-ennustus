from pyproj import Transformer

# WGS84 lat/lon -> Web Mercator (meters). Adjust if you prefer local UTM.
_TO_M = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
_FROM_M = Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True)

def lonlat_to_xy(lon, lat):
    x,y = _TO_M.transform(lon, lat)
    return x,y

def xy_to_lonlat(x, y):
    lon,lat = _FROM_M.transform(x, y)
    return lon,lat