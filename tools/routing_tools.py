import os, requests
import json
import math

from pydantic_ai import RunContext
# from datastructures import MyDeps


#def location_to_coordinates(ctx: RunContext[MyDeps], location: str):
def get_coordinates(location: str) -> tuple[float, float]:
    """Get the geographical coordinates of a location
    Args:
        location : the location of which you want to obtain the coordinates
    Returns:
        (latitude, longitude)
    Examples:
        ```python
        get_coordinates("Pradamano")
        get_ccordinates("Via delle scienze 206, Udine")
        ```
    """
    params = {
        "q": f"{location}",
        "format": "json"
    }
    headers = {
        "User-Agent": "cycling-trip-acency, route_planner"  
    }
    url = f"https://nominatim.openstreetmap.org/search"

    response = requests.get(url, params=params, headers=headers)
        
    if response.status_code == 200:
        json_response = response.json()[0]
        coordinates = (json_response["lat"], json_response["lon"])
    else:
        print(f"In location_to_coordinates\nInput: \n\tlocation: {location}\nRequest returned with conde: {response.status_code}")
        coordinates = tuple()

    return coordinates


def get_route(locations_coordinates: list[tuple[float, float]], idx: int) -> list[list[float]]:
    route = []
    for i in range(1, len(locations_coordinates)):
        lonlats_string = f"{locations_coordinates[i-1][1]},{locations_coordinates[i-1][0]}|{locations_coordinates[i][1]},{locations_coordinates[i][0]}"
        url = f"http://localhost:17777/brouter?lonlats={lonlats_string}&profile=fastbike&alternativeidx={idx}&format=geojson"
        response = requests.get(url)

        if response.status_code == 200:
            route.extend(response.json()["features"][0]["geometry"]["coordinates"])
        else:
            print(f"In get_routing_informations\nInput: \n\tlocations_coordinates: {locations_coordinates}\nRequest returned with conde: {response.status_code}")

    return route


def get_routes(locations_coordinates: list[tuple[float, float]]) -> list[list[list[float]]]:
    """Get 4 different routes that goes through the locations provided
    Args:
        locations_coordinates : list of locations coordinate
    Returns:
        list containing 4 different routes
    Examples:
        ```python
        get_routes([('46.0634632', '13.2358377'), ('45.9562503', '12.6597197')])
        get_routes([('46.0634632', '13.2358377'), ('45.9562503', '12.6597197'), ('46.0306995', '12.5016263'), ('45.9538600', '12.5033680')])
        ```
    """
    routes = []
    for idx in range(0, 4):
        routes.append(get_route(locations_coordinates, idx))
    return routes


def geo_point_distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    """
    Args:
        a : (latitude_a, longitude_a)
        b : (latitude_b, longitude_b)
    Returns:
        geographical distance between point a and point b calculated using Federal Communication Commission formula (for distances not over 475 km)
    """
    lat_a, lon_a, _ = a
    lat_b, lon_b, _ = b

    difference_in_lon = lon_a - lon_b
    difference_in_lat = lat_a - lat_b

    mean_latitude = (lat_a + lat_b) / 2

    K1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
    K2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

    D = math.sqrt(math.pow(K1 * difference_in_lat, 2) + math.pow(K2 * difference_in_lon, 2))
    
    return D


def lon_lat_elv_point_distance(a: list[float], b: list[float]) -> float:
    """
    Args:
        a: [longitude_a, latitude_a, elvevation_a]
        b: [longitude_b, latitude_b, elevation_a]
    Returns:
        geographical distance between point a and point b calculated using Federal Communication Commission formula (for distances not over 475 km)
    """
    lat_a, lon_a, _ = a
    lat_b, lon_b, _ = b

    difference_in_lon = lon_a - lon_b
    difference_in_lat = lat_a - lat_b

    mean_latitude = (lat_a + lat_b) / 2

    K1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
    K2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

    D = math.sqrt(math.pow(K1 * difference_in_lat, 2) + math.pow(K2 * difference_in_lon, 2))
    
    return D


def divide_path(coordinates: list[list[float]], km_per_day: int) -> list[list[list[float]]]:
    division = []
    idx = 1

    # TODO check the idx guards
    while idx < len(coordinates):
        track = [coordinates[idx-1]]
        distance = 0
        
        while distance < km_per_day:
            if idx < len(coordinates):
                track.append(coordinates[idx])
                distance += lon_lat_elv_point_distance(coordinates[idx-1], coordinates[idx])
                idx += 1
            else:
                break

        division.append(track)

    return division


def fill_trip_descriptor():
    ...

locations = ["Pordenone", "Polcenigo", "Sacile"]
locations_coordinates = [get_coordinates(loc) for loc in locations]
print(locations_coordinates)
routes = get_routes(locations_coordinates)
selected_route = routes[1]
km_per_day = 20
route_division = divide_path(selected_route, km_per_day)
for d in route_division : print(d)