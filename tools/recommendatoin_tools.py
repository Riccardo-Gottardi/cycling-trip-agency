import requests, os, sys, time, math
from pydantic_ai import RunContext

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from datastructures.dependencies import MyDeps
from datastructures.Place import Place
from dataclasses import dataclass
from datastructures.TripDescriptor import TripDescriptor
from datastructures.UserDescriptor import UserDescriptor
from datastructures.Recommendation import Recommendation


@dataclass
class Context:
    deps: MyDeps

def query_overpass(query: str, max_retries: int = 3) -> requests.Response | None:
    url = "https://overpass-api.de/api/interpreter"

    for i in range(max_retries):
        try:
            response = requests.post(url, data=query, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            if response.status_code != 200:
                time.sleep(2**i)
                continue
            return response
        except:
            if i == max_retries - 1:
                return None


def get_amenity_pois(search_center: list[float], search_radius: int, amenityes: dict) -> list[Place]:
    lan, lon, _ = search_center

    query = "[out:json][timeout:25];("

    for key in amenityes.keys():
        query += f'node["amenity"="{key}"]["name"~"{"".join(v+"|" for v in amenityes.get(key))}"](around:{search_radius},{lan},{lon});' # pyright: ignore[reportOptionalIterable]

    query += ");out geom qt 10;"

    data = query_overpass(query)
    places = []

    if data:
        data = data.json()
        
        for d in data.get("elements"):
            name = d.get("tags").get("name")
            addr_city = d.get("tags").get("addr:city")

            if name and addr_city:
                place = Place(name=f"{name}, {addr_city}")
                if place.get_name():
                    places.append(place)

    return places

def fcc_discance(a: list[float], b: list[float]) -> float:
        lat_a, lon_a, _ = a
        lat_b, lon_b, _ = b

        difference_in_lon = lon_a - lon_b
        difference_in_lat = lat_a - lat_b

        mean_latitude = (lat_a + lat_b) / 2

        K1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
        K2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

        D = math.sqrt(math.pow(K1 * difference_in_lat, 2) + math.pow(K2 * difference_in_lon, 2))
        
        return D * 1000

def get_route_recommedations(ctx: Context, search_radius: int = 10000) -> str | None:
    candidate_routes = ctx.deps.trip.get_candidate_routes()
    selected_route = ctx.deps.trip.get_selected_route()

    if candidate_routes and selected_route:
        recommendations = []
        previous_point = candidate_routes[selected_route][0]
        distance_from_previous_search_point = search_radius

        for p in candidate_routes[selected_route][1:]:
            increment = fcc_discance(previous_point, p)
            if distance_from_previous_search_point + increment >= 2*search_radius:
                recommendations.extend(get_amenity_pois(p, search_radius, {}))
                distance_from_previous_search_point = 0.0

        return str(recommendations)

def plan_candidate_route(ctx: Context) -> str | None:
    """A function to plan the candidate route for the trip.
    Returns:
        - list[list[list[float]]] | str: The planned candidate route or an error message.
    Example:
        ```python
        candidate = plan_candidate_route(ctx)
        ```
    """
    ret = ctx.deps.trip.plan_candidate_routes()
    if ret is not None:
        return ret


ctx = Context(MyDeps(TripDescriptor(), UserDescriptor(), Recommendation()))
ctx.deps.trip.fill(
    bike_type="gravel",
    places=["Pordenone", "Sacile"]
)

amenity = {
    "restaurant": ["Greek", "Chinese"]
    }

res = plan_candidate_route(ctx)
if not res:
    recommendations = get_route_recommedations(ctx)
    print(recommendations)
else:
    print(res)