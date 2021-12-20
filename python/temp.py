muni_tiles_json = oauth.get(BASE_URL + "/grids/municipalities/{0}".format(municipality), headers = headers).json()
len(muni_tiles_json["tiles"])
type(muni_tiles_json)
type(muni_tiles_json["tiles"])

tile_ids = [t["tileId"] for t in muni_tiles_json["tiles"]]
type(tile_ids)
len(tile_ids)


import json

with open('data/swisscom/chansy_grid.json', 'w', encoding = 'utf-8') as f:
    json.dump(muni_tiles_json, f, ensure_ascii = False, indent = 4) 