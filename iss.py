import requests
from colorzero import Color
import json


def get_iss_colour():
    response = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
    response.raise_for_status()  # Raises an exception if HTTP status != 200
    obj = response.json()        # Automatically parses JSON

    lat = float(obj['iss_position']['latitude'])
    lon = float(obj['iss_position']['longitude'])
    print(f"iss position = ({lon}, {lat})")

    # --- Map to HSV ---
    #h = (lon + 180.0) / 360.0
    #s = 1.0
    #v = 0.4 + 0.6 * abs(lat) / 90.0

    h = (lon + 180.0) / 360.0
    #h += 0.02 * (lat / 90.0)
    #PERLIN_AMPLITUDE = 0.25 + 0.2 * (1 - abs(lat) / 90.0)
    s = 0.6 + 0.4 * (1 - abs(lat)/90.0)
    v = 1.0



    return Color.from_hsv(h, s, v)

