from pydantic import BaseModel, Field
from datetime import date


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometer_per_day: int = Field(default=0, description="the maximum amout of kilometers the user is able to ride in a day")
    difference_in_height_per_day: int = Field(default=0, description="the maximum difference of height in meter the user is ablo do in a day")

    def get_kilometer_per_day(self) -> int:
        return self.kilometer_per_day
    
    def get_difference_in_height_per_day(self) -> int:
        return self.difference_in_height_per_day

    def fill(self, things: dict):
        for key in things.keys():
            if key == "kilometer_per_day":
                assert isinstance(things["kilometer_per_day"], int), f"in PerformanceDescriptor.fill()\nThe given kilometer_per_day must be of type integer\n{things['kilometer_per_day'].__class__} was provided"
                self.kilometer_per_day = things["kilometer_per_day"]
            elif key == "difference_in_height_per_day":
                assert isinstance(things["difference_in_height_per_day"], int), f"in PerformanceDescriptor.fill()\nThe given difference_in_height_per_day must be of type integer\n{things['difference_in_height_per_day'].__class__} was provided"
                self.difference_in_height_per_day = things["difference_in_height_per_day"]
            else:
                print(f"Warning: {key}, unexisting key was used when filling the performance descriptor")

    def debug_dict(self) -> dict:
        return {
            "kilometer_per_day": {"class": self.get_kilometer_per_day().__class__, "value": self.get_kilometer_per_day()},
            "difference_in_height_per_day": {"class": self.get_difference_in_height_per_day().__class__, "value": self.get_difference_in_height_per_day()}
        }


class  PreferencesDescriptor(BaseModel):
    """Preference of the user for the points of interest"""
    amenity: list[str] | None = Field(default=None, description="")
    turism: list[str] | None = Field(default=None, description="")
    historic: list[str] | None = Field(default=None, description="")
    natural: list[str] | None = Field(default=None, description="")
    water: list[str] | None = Field(default=None, description="")
    laisure: list[str] | None = Field(default=None, description="")
    man_made: list[str] | None = Field(default=None, description="")
    q: list[str] | None = Field(default=None, description="")

    def fill(self, things: dict) -> None:
        for key in things.keys():
            if key == "amenity":
                assert isinstance(things["amenity"], list), f"in PreferencesDescriptor.fill()\nThe given amenity must be of type list\n{things['amenity'].__class__} was provided"
                self.amenity = things["amenity"]
            elif key == "turism":
                assert isinstance(things["turism"], list), f"in PreferencesDescriptor.fill()\nThe given turism must be of type list\n{things['turism'].__class__} was provided"
                self.turism = things["turism"]
            elif key == "historic":
                assert isinstance(things["historic"], list), f"in PreferencesDescriptor.fill()\nThe given historic must be of type list\n{things['historic'].__class__} was provided"
                self.historic = things["historic"]
            elif key == "natural":
                assert isinstance(things["natural"], list), f"in PreferencesDescriptor.fill()\nThe given natural must be of type list\n{things['natural'].__class__} was provided"
                self.natural = things["natural"]
            elif key == "water":
                assert isinstance(things["water"], list), f"in PreferencesDescriptor.fill()\nThe given water must be of type list\n{things['water'].__class__} was provided"
                self.water = things["water"]
            elif key == "laisure":
                assert isinstance(things["laisure"], list), f"in PreferencesDescriptor.fill()\nThe given laisure must be of type list\n{things['laisure'].__class__} was provided"
                self.laisure = things["laisure"]
            else:
                print(f"Warning: {key}, unexisting key was used when filling the preferences descriptor")

    def to_one_hot_encoding(self) -> set:
        """Convert the preferences to a one-hot encoding dictionary"""
        one_hot = set()
        if self.amenity is not None:
            one_hot.update(self.amenity)
        if self.turism is not None:
            one_hot.update(self.turism)
        if self.historic is not None:
            one_hot.update(self.historic)
        if self.natural is not None:
            one_hot.update(self.natural)
        if self.water is not None:
            one_hot.update(self.water)
        if self.laisure is not None:
            one_hot.update(self.laisure)
        if self.man_made is not None:
            one_hot.update(self.man_made)
        if self.q is not None:
            one_hot.update(self.q)
        return one_hot


class UserDescription(BaseModel):
    """Description of the user"""
    performance: PerformanceDescriptor = Field(default=PerformanceDescriptor(), description="measure of the user cycling performance of the user")
    preferences: PreferencesDescriptor = Field(default=PreferencesDescriptor(), description="preferences of the user for the points of interest")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Check if the user exist in the persistance system
        # If yes, load his performance and preferences
        # If no, do nothing

    def fill(self, things: dict) -> None:
        for key in things.keys():
            if key == "performance":
                assert isinstance(things["performance"], dict), f"in UserDescription.fill()\nThe given performance must be of type dict\n{things['performance'].__class__} was provided"
                self.performance.fill(things["performance"])
            elif key == "preferences":
                assert isinstance(things["preferences"], dict), f"in UserDescription.fill()\nThe given preferences must be of type dict\n{things['preferences'].__class__} was provided"
                self.preferences.fill(things["preferences"])
            else:
                print(f"Warning: {key}, unexisting key was used when filling the user description")


class Place(BaseModel):
    """Represent a place"""
    name: str = Field(default="", description="name of the place, it can be a city, a street, a point of interest, etc.")
    lat: float | None = Field(default=None, description="latitude of the place, if None, it will be set automatically")
    lon: float | None = Field(default=None, description="longitude of the place, if None, it will be set automatically")
    elv: float | None = Field(default=None, description="elevation of the place, if None, it will be set automatically")

    def model_post_init(self, __context__=None) -> None:
        self.__set_coordinates(self.name)

    def __set_coordinates(self, location: str) -> None:
        import requests
        
        params = {
            "q": f"{location}",
            "format": "json"
        }
        headers = {
            "User-Agent": "cycling-trip-acency, Place class"  
        }
        url = f"https://nominatim.openstreetmap.org/search"

        response = requests.get(url, params=params, headers=headers)
            
        if response.status_code == 200:
            json_response = response.json()[0]
            self.lat, self.lon = json_response["lat"], json_response["lon"]
        else:
            print(f"In Place.__set_coordinates\nInput: \n\tlocation: {location}\nRequest returned with code: {response.status_code}")

    def get_name(self) -> str:
        """Get the name of the place"""
        return self.name

    def get_coordinates(self) -> tuple[float, float, float]:
        """Get the coordinates of the place"""
        if self.lat is None or self.lon is None:
            raise ValueError("Coordinates are not set")
        return (self.lat, self.lon, self.elv) if self.elv is not None else (self.lat, self.lon, 0.0)    


# TODO add automatic logic for route planning, once places are set
# triggered every time places is updated -> when places is filled
class RouteDescriptor(BaseModel):
    """Description of the route of the trip"""
    places: list[Place] = Field(default=[], description="list of places, the first is the starting point, the last is the ending point")
    candidate_raw_route: list[list[list[float]]] | None = Field(default=None, description="list of candidate raw routes, each route is a list of geopoints, each geopoint is a list of 3 coordinates (lat, lon, elv)")
    selected_raw_route: int | None = Field(default=None, description="index of the selected raw route, if None, no route was selected")
    stepped_route: list[list[list[float]]] | None = Field(default=None, description="division of the trip as segments, list of geographical positions")
    length: float | None = Field(default=None, description="length of the route in meters")

    def fill(self, things: dict) -> None:
        for key in things.keys():
            if key == "places":
                assert isinstance(things["places"], list), f"in RouteDescriptor.fill()\nThe given places must be of type list, list of place\n{things['places'].__class__} was provided"
                assert len(things["places"]) > 2, f""
                assert isinstance(things["places"][0], str), f"in RouteDescriptor.fill()\nThe given places element must be of type str\n{things['places'][0].__class__} was provided"
                self.places = things["places"]
                self.__plan_raw_route()
            
            elif key == "raw_route":
                assert isinstance(things["raw_route"], list), f"in RouteDescriptor.fill()\nThe given raw_route must be of type list, list of geopoints\n{things['raw_route'].__class__} was provided"
                if len(things["raw_route"]) > 0 : assert isinstance(things["raw_route"][0], list), f"in RouteDescriptor.fill()\nThe given raw_route elements must be of type list, list of coordinate\n{things['raw_route'][0].__class__} was provided"
                if len(things["raw_route"][0]) > 0 : assert isinstance(things["raw_route"][0][0], float), f"in RouteDescriptor.fill()\nThe given raw_route elements elements must be of type float, a coordinate\n{things['raw_route'][0][0].__class__} was provided"
                self.raw_route = things["raw_route"]
            
            elif key == "stepped_route":
                assert isinstance(things["stepped_route"], list), f"in RouteDescriptor.fill()\nThe given stepped_route must be of type list, list of segments\n{things['stepped_route'].__class__} was provided"
                if len(things["stepped_route"]) > 0 : assert isinstance(things["stepped_route"][0], list), f"in RouteDescriptor.fill()\nThe given stepped_route elements must be of type list, list of geopoints(list of 3 coordinates)\n{things['stepped_route'][0].__class__} was provided"
                if len(things["stepped_route"][0]) > 0 : assert isinstance(things["stepped_route"][0][0], list), f"in RouteDescriptor.fill()\nThe given stepped_route elements elements must be of type list, geopoints(list of 3 coordinates)\n{things['stepped_route'][0][0].__class__} was provided"
                if len(things["stepped_route"][0][0]) > 0 : assert isinstance(things["stepped_route"][0][0][0], float), f"in RouteDescriptor.fill()\nThe given stepped_route elements elements elements must be of type float, coortinates of a geopoints(list of 3 coordinates)\n{things['stepped_route'][0][0][0].__class__} was provided"
                self.stepped_route = things["stepped_route"]
            
            elif key == "length":
                assert isinstance(things["length"], float), f"in RouteDescriptor.fill()\nThe given length must be of type float\n{things['length'].__class__} was provided"
                self.length = things["length"]

            else:
                print(f"Warning: {key}, unexisting key was used when filling the route descriptor")

    def __plan_raw_route(self) -> None:
        ...

    def __get_route(self, idx: int) -> list[list[float]]:
        """Get the route from the places"""
        import requests

        locations_coordinates = [place.get_coordinates() for place in self.places]
        route = []
        for i in range(1, len(locations_coordinates)):
            lonlats_string = f"{locations_coordinates[i-1][1]},{locations_coordinates[i-1][0]}|{locations_coordinates[i][1]},{locations_coordinates[i][0]}"
            url = f"http://localhost:17777/brouter?lonlats={lonlats_string}&profile=fastbike&alternativeidx={idx}&format=geojson"
            response = requests.get(url)

            if response.status_code == 200:
                route.extend(response.json()["features"][0]["geometry"]["coordinates"])
            else:
                print(f"In RouteDescriptor.__get_route\nInput: \n\tlocations_coordinates: {locations_coordinates}\nRequest returned with code: {response.status_code}")

        return route
    
    def __get_routes(self) -> list[list[list[float]]]:
        """Get 4 different routes that goes through the places provided"""
        routes = []
        for i in range(4):
            route = self.__get_route(i)
            if len(route) > 0:
                routes.append(route)
        return routes
    
    def __geopoint_distance(self, a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
        """Calculate the geographical distance between two points using the Federal Communication Commission formula (for distances under 475 km)"""
        import math

        lat_a, lon_a, _ = a
        lat_b, lon_b, _ = b

        difference_in_lon = lon_a - lon_b
        difference_in_lat = lat_a - lat_b

        mean_latitude = (lat_a + lat_b) / 2

        K1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
        K2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

        D = math.sqrt(math.pow(K1 * difference_in_lat, 2) + math.pow(K2 * difference_in_lon, 2))
        
        return D
    
    # TODO adjust calculations, some types are not correct
    def plan_steps(self, max_distance: float = 10000.0) -> None:
        """
        Plan the steps of the route based on the maximum distance
        Args:
            max_distance : maximum distance in meters for each step, default is 10000.0 (10 km)
        """
        if self.candidate_raw_route is None:
            self.candidate_raw_route = self.__get_routes()
        
        if len(self.candidate_raw_route) == 0:
            print("No candidate raw route found")
            return
        
        self.stepped_route = []
        current_step = []
        current_distance = 0.0
        
        for segment in self.candidate_raw_route[0]:
            if len(segment) < 2:
                continue
            
            for i in range(len(segment) - 1):
                point_a = segment[i]
                point_b = segment[i + 1]
                distance = self.__geopoint_distance(point_a, point_b)
                
                if current_distance + distance > max_distance:
                    if current_step:
                        self.stepped_route.append(current_step)
                    current_step = [point_a]
                    current_distance = distance
                else:
                    current_step.append(point_a)
                    current_distance += distance
            
            if current_step:
                current_step.append(segment[-1])
        
        if current_step:
            self.stepped_route.append(current_step)


        

class TripDescriptor(BaseModel):
    """Description of a bycicle trip"""
    ride_type: str = Field(default="", description="either ONE_WAY or LOOP. Tell if the starting point is also the ending point, or not")
    bicycle_profile: str = Field(default="", description="either ROAD, GRAVEL, MTB. Is the type of byke")
    number_of_days: int = Field(default=0, description="the number of days the trip will last")
    dates: list[date] | None = Field(default=None, description="starting and ending date of the trip")
    route: RouteDescriptor = Field(default=RouteDescriptor(), description="")
    stepped_route: list[list[list[float]]] | None = Field(default=None, description="division of the trip as segments, list of geographical positions")

    def get_ride_type(self) -> str:
        return self.ride_type
    
    def get_bicycle_profile(self) -> str:
        return self.bicycle_profile
    
    def get_number_of_days(self) -> int:
        return self.number_of_days
    
    def get_dates(self) -> list[date] | None:
        return self.dates
    
    def get_route(self) -> RouteDescriptor:
        return self.route
    
    def get_stepped_route(self) -> list[list[list[float]]] | None:
        return self.stepped_route

    def fill(self, things: dict) -> None:
        for key in things.keys():
            if key == "ride_type":
                assert isinstance(things["ride_type"], str), f"in TripDescriptor.fill()\nThe given ride_type must be of type string\n{things['ride_type'].__class__} was provided"
                self.ride_type = things["ride_type"]

            elif key == "bicycle_profile":
                assert isinstance(things["bicycle_profile"], str), f"in TripDescriptor.fill()\nThe given bicycle_profile must be of type string\n{things['bicycle_profile'].__class__} was provided"
                assert things["bicycle_profile"] in ["ROAD", "GRAVEL", "MTB"], f"in TripDescriptor.fill()\nThe given bicycle_profile must be one of the following: ROAD, GRAVEL, MTB\n{things['bicycle_profile']} was provided"
                self.bicycle_profile = things["bicycle_profile"]
                
            elif key == "number_of_days":
                assert isinstance(things["number_of_days"], int), f"in TripDescriptor.fill()\nThe given number_of_days must be an of type integer\n{things['number_of_days'].__class__} was provided"
                assert things["number_of_days"] > 0, f"in TripDescriptor.fill()\nThe given number_of_days must be greater than 0\n{things['number_of_days']} was provided"
                self.number_of_days = things["number_of_days"]

            elif key == "dates":
                assert isinstance(things["dates"], list), f"in TripDescriptor.fill()\nThe given dates must be of type list\n{things['dates'].__class__} was provided"
                if len(things["dates"]) > 0 : assert isinstance(things["dates"][0], date), f"in TripDescriptor.fill()\nThe given dates elements must be of type date\n{things['dates'][0].__class__} was provided"
                self.dates = things["dates"]

            elif key == "route":
                self.route.fill(things["route"])

            elif key == "stepped_route":
                assert isinstance(things["stepped_route"], list), f"in TripDescriptor.fill()\nThe given stepped_route must be of type list, list of segments\n{things['stepped_route'].__class__} was provided"
                if len(things["stepped_route"]) > 0 : assert isinstance(things["stepped_route"][0], list), f"in TripDescriptor.fill()\nThe given stepped_route elements must be of type list, list of geopoints(list of 3 coordinates)\n{things['stepped_route'][0].__class__} was provided"
                if len(things["stepped_route"][0]) > 0 : assert isinstance(things["stepped_route"][0][0], list), f"in TripDescriptor.fill()\nThe given stepped_route elements elements must be of type list, geopoints(list of 3 coordinates)\n{things['stepped_route'][0][0].__class__} was provided"
                if len(things["stepped_route"][0][0]) > 0 : assert isinstance(things["stepped_route"][0][0][0], float), f"in TripDescriptor.fill()\nThe given stepped_route elements elements elements must be of type float, coortinates of a geopoints(list of 3 coordinates)\n{things['stepped_route'][0][0][0].__class__} was provided"
                self.stepped_route = things["stepped_route"]

            else:
                print(f"Warning: {key}, unexisting key was used when filling the trip descriptor")

    def debug_dict(self) -> dict:
        return {
            "ride_type": {"class": self.get_ride_type().__class__, "value": self.get_ride_type()},
            "bicycle_profile": {"class": self.get_bicycle_profile().__class__, "value": self.get_bicycle_profile()},
            "number_of_days": {"class": self.get_number_of_days().__class__, "value": self.get_number_of_days()},
            "dates": {"class": self.get_dates().__class__, "value": self.get_dates()},
            "route": {"class": self.get_route().__class__, "value": self.get_route()},
            "stepped_route": {"class": self.get_stepped_route().__class__, "value": self.get_stepped_route()},
        }
    