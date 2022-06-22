# -*- coding: utf-8 -*-
"""
Accessing  http://digital.swisscom.com API platform

Example derived from https://github.com/swisscom/mip/blob/master/query_swisscom_heatmaps_api.py
"""

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime import datetime, timedelta
import pprint

import json

BASE_URL = "https://api.swisscom.com/layer/heatmaps/demo"
TOKEN_URL = "https://consent.swisscom.com/o/oauth2/token"
MAX_NB_TILES_REQUEST = 100
headers = {"scs-version": "2"}  # API version


# credentials
keys_file = open("../secrets/swisscom.txt")
lines = keys_file.readlines()

# heatmaps specific
client_id = lines[2].rstrip()
client_secret = lines[4].rstrip()

# dwell time specific
# client_id = lines[7].rstrip()
# client_secret = lines[9].rstrip()


# Fetch an access token
client = BackendApplicationClient(client_id = client_id)
oauth = OAuth2Session(client = client)
oauth.fetch_token(token_url = TOKEN_URL, client_id = client_id, client_secret = client_secret)


# **Chansy** to define `x`
# Postal code	1284
# SFOS number	6611
municipality = 6611
muni_tiles_json = oauth.get(
    BASE_URL + "/grids/municipalities/{0}".format(municipality), headers = headers
).json()

type(muni_tiles_json)
type(muni_tiles_json["tiles"])
len(muni_tiles_json["tiles"])

muni_tiles_json.items()
muni_tiles_json["tiles"][1]

# save grid to json
with open('data/swisscom/chansy_grid.json', 'w', encoding = 'utf-8') as f:
    json.dump(muni_tiles_json, f, ensure_ascii = False, indent = 4) 

# **Chiasso** to define `y`  
# Postal code `6830`
# SFOS number	`5250`
municipality = 5250
muni_tiles_json = oauth.get(
    BASE_URL + "/grids/municipalities/{0}".format(municipality), headers = headers
).json()

len(muni_tiles_json["tiles"])

# save grid to json
with open('data/swisscom/chiasso_grid.json', 'w', encoding = 'utf-8') as f:
    json.dump(muni_tiles_json, f, ensure_ascii = False, indent = 4) 

# **Bern PLZs** to capture city centre

# Postal code	3066
plz = 3066
ply_tiles_json = oauth.get(
    BASE_URL + "/grids/postal-code-areas/{0}".format(plz), headers = headers
).json()

type(ply_tiles_json)
type(ply_tiles_json["tiles"])
len(ply_tiles_json["tiles"])

ply_tiles_json.items()
ply_tiles_json["tiles"][1]

# save grid to json
with open('../data/swisscom/grid_3066.json', 'w', encoding = 'utf-8') as f:
    json.dump(ply_tiles_json, f, ensure_ascii = False, indent = 4) 

# Get all the first MAX_NB_TILES_REQUEST tile ids associated with the municipality  of interest

tile_ids = [t["tileId"] for t in muni_tiles_json["tiles"]][
    :MAX_NB_TILES_REQUEST
]

type(tile_ids)
len(tile_ids)

# define a start time and request the density for the following given number of hours
start_time = datetime(year=2020, month=1, day=27, hour=0, minute=0)
dates = [(start_time + timedelta(hours=delta)) for delta in range(24)]
date2score = dict()

for dt in dates:
    api_request = (
        BASE_URL
        + "/heatmaps/dwell-density/hourly/{0}".format(dt.isoformat())
        + "?tiles="
        + "&tiles=".join(map(str, tile_ids))
    )
    daily_total_density = sum(
        map(
            lambda t: t["score"],
            oauth.get(api_request, headers = headers).json()["tiles"],
        )
    )
    date2score[dt.isoformat()] = daily_total_density

# print the daily density for every date
print("The average hourly density for postal code {0}".format(municipality))
pprint.PrettyPrinter(indent=4).pprint(date2score)
