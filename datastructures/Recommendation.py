import requests, time, random
from pydantic import BaseModel
from datastructures.Place import Place
from datastructures.DistanceCalculation import DistanceCalculation


class Recommendation(BaseModel):
    recommended_places: list[Place] = []

    def get_recommended_places(self) -> list[Place]:
        return self.recommended_places

    @classmethod
    def __query_overpass(cls, query: str, max_retries: int = 3) -> requests.Response: # pyright: ignore[reportReturnType]
        url = "https://overpass-api.de/api/interpreter"

        for i in range(max_retries):
            try:
                response = requests.post(url, data=query, headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
                response.raise_for_status()
                return response
            except Exception as e:
                if i != max_retries - 1:
                    time.sleep(2 ** i + random.uniform(0, 1))
                    continue
                raise e

    def __get_amenity_pois(self, search_center: list[float], search_radius: int, amenities: dict) -> list[Place]:
        lon, lat, _ = search_center

        query = "[out:json][timeout:25];("

        for key in amenities.keys():
            a = amenities.get(key)
            if a is not None:
                query += f'node["amenity"="{key}"]["name"~"{"".join(v+"|" for v in a[:len(a)-1])}{a[-1]}"](around:{search_radius},{lat},{lon});' # pyright: ignore[reportOptionalIterable]

        query += ");out geom qt 10;"

        try:
            data = self.__query_overpass(query)
        except Exception as e:
            raise e

        recommended_places = []

        if data:
            data = data.json()
            
            i = 0
            for d in data.get("elements"):
                if i == 3: # Limit the pois to 3 results
                    break
                name = d.get("tags").get("name")
                addr_city = d.get("tags").get("addr:city")

                if name and addr_city:
                    place = Place(name=f"{name}, {addr_city}")
                    if place.get_name():
                        recommended_places.append(place)
                        i += 1

        return recommended_places

    def find_route_recommendations(self, route: list[list[float]], amenity: dict, search_radius: int = 10000) -> None:
        self.recommended_places = []
        distance_from_previous_search_point = search_radius

        for i in range(1, len(route)):
            distance_from_previous_search_point += DistanceCalculation.fcc_distance(route[i-1], route[i])
            if distance_from_previous_search_point >= 2*search_radius:
                try: 
                    pois = self.__get_amenity_pois(route[i], search_radius, amenity)
                except Exception as e:
                    raise e
                self.recommended_places.extend(pois)
                distance_from_previous_search_point = 0.0
