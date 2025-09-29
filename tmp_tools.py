import requests
from datastructures.Place import Place
from datastructures.DistanceCalculation import DistanceCalculation

"""
Udine coordinates: 46.063862, 13.236718

[out:json][timeout:25];
// Bounding box: south, west, north, east (example numbers)
(
  node["place"~"city|town|village"](45.5, 12.0, 46.0, 13.0);
);
out body;
"""

def get_place_suggestions(place_cord: list[float], radius: int) -> list: 
	"""Given a point and a radius it return 10 city in the area of radius radius from the place at place_cord"""
	url = "https://overpass-api.de/api/interpreter"
	query = f"[out:json][timeout:25];node[\"place\"~\"city|town\"](around:{radius},{place_cord[0]},{place_cord[1]});out geom qt 10;"

	response = requests.post(url, data={"data": query}, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
	response.raise_for_status()

	data = response.json()
	return data.get("elements")


# 12 -> town/borough
# 13 -> village/suburb
tarvisio = Place(name="Tarvisio")
grado = Place(name="Grado")
ud_cord = (46.063862, 13.236718)


def get_intermediate_city_suggestions(a: list[float], b: list[float]):
	radius = DistanceCalculation.fcc_distance(a, b) * 1000 / 2
	point = [
		a[0] + (b[0] - a[0])/2, 
		a[1] + (b[1] - a[1])/2
	]

	url = f"https://nominatim.openstreetmap.org/reverse"
	headers = {
		"User-Agent": "cycling-trip-agency, tmp file"  
	}
	params = {
		"lat": point[0],
		"lon": point[1],
		"zoom": 12 ,
		"format": "json",
		"addressdetail": 1
	}

	response = requests.get(url, params=params, headers=headers)
	response.raise_for_status()
	data = response.json()

	return get_place_suggestions([data.get("lat"), data.get("lon")], int(radius))


cities = get_intermediate_city_suggestions(tarvisio.get_coordinates(), grado.get_coordinates())
for c in cities : 
	name_it = c.get("tags").get("name:it")
	if name_it:
		print(name_it, end="\n\n")
	else:
		print(c.get("tags").get("name"), end="\n\n")