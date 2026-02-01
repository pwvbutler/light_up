import requests
from colorzero import Color

cheerlights_url = "http://api.thingspeak.com/channels/1417/field/2/last.txt"

def get_cheerlights_colour():
    resp = requests.get(cheerlights_url, timeout=2)
    c = Color(resp.content)

    return c

