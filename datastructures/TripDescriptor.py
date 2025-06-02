from pydantic import BaseModel, Field
from datetime import date


class Place(BaseModel):
    """Represent a place
    Args:
        name (str): name of the place, it can be a city, a street, a point of interest, etc.
        lat (float | None): latitude of the place, if None, it will be set automatically
        lon (float | None): longitude of the place, if None, it will be set automatically
        elv (float | None): elevation of the place, if None, it will be set automatically
    Examples:
    ```python
    udine = Place("Udine")
    louis_pordenone = Place("Louis, Pordenone")
    ```
    """
    name: str = Field(description="name of the place, it can be a city, a street, a point of interest, etc.")
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


class TripDescriptor(BaseModel):
    """Description of a bycicle trip
    Args:
        ride_type (str): either one_way or loop. Tell if the starting point is also the ending point, or not
        bicycle_profile (str): either road, gravel, mtb. Is the type of byke
        number_of_days (int): the number of days the trip will last
        dates (list[date] | None): starting and ending date of the trip
        places (list[Place]): list of places, the first is the starting point, the last is the ending point
        candidate_raw_routes (list[list[list[float]]] | None): list of candidate raw routes, each route is a list of geopoints, each geopoint is a list of 3 coordinates (lat, lon, elv)
        selected_raw_route (int | None): index of the selected raw route, if None, no route was selected
        stepped_route (list[list[list[float]]] | None): division of the trip as segments, list of geographical positions
        length (float | None): length of the route in meters
    Examples:
    ```python
    trip = TripDescriptor()
    trip.fill({
        "ride_type": "one_way",
        "bicycle_profile": "gravel",
        "number_of_days": 4,
    })
    trip.fill({"places": ["Udine", "Palmanova", "Trieste"]})
    candidate_routes = trip.get_candidate_raw_routes()
    ...
    trip.fill({"selected_raw_route": 0})
    """
    ride_type: str = Field(default="", description="either one_way or loop. Tell if the starting point is also the ending point, or not")
    bicycle_profile: str = Field(default="", description="either road, gravel, mtb. Is the type of byke")
    number_of_days: int = Field(default=0, description="the number of days the trip will last")
    dates: list[date] | None = Field(default=None, description="starting and ending date of the trip")
    places: list[Place] = Field(default=[], description="list of places, the first is the starting point, the last is the ending point")
    candidate_raw_routes: list[list[list[float]]] | None = Field(default=None, description="list of candidate raw routes, each route is a list of geopoints, each geopoint is a list of 3 coordinates (lat, lon, elv)")
    selected_raw_route: int | None = Field(default=None, description="index of the selected raw route, if None, no route was selected")
    stepped_route: list[list[list[float]]] | None = Field(default=None, description="division of the trip as segments, list of geographical positions")
    length: float | None = Field(default=None, description="length of the route in meters")

    def get_ride_type(self) -> str:
        """Get the type of ride"""
        return self.ride_type
    
    def get_bicycle_profile(self) -> str:
        """Get the type of bicycle"""
        return self.bicycle_profile
    
    def get_number_of_days(self) -> int:
        """Get the number of days of the trip"""
        return self.number_of_days
    
    def get_dates(self) -> list[date] | None:
        """Get the list of dates of the trip"""
        return self.dates
    
    def get_places(self) -> list[Place]:
        """Get the list of places"""
        return self.places
    
    def get_candidate_raw_routes(self) -> list[list[list[float]]] | None:
        """Get the list of candidate raw routes"""
        return self.candidate_raw_routes
    
    def get_selected_raw_route(self) -> int | None:
        """Get the index of the selected raw route"""
        return self.selected_raw_route
    
    def get_stepped_route(self) -> list[list[list[float]]] | None:
        """Get the list of segments of the route"""
        return self.stepped_route
    
    def get_length(self) -> float | None:
        """Get the length of the route in meters"""
        return self.length
    
    def fill(self, things: dict) -> None:
        """Fill the TripDescriptor with the given things
        Args:
            things (dict): dictionary with the attributes to fill the TripDescriptor with. Key is the attribute name, value is the attribute value. settable attributes are:
                - ride_type (str): either one_way or loop. Tell if the starting point is also the ending point, or not
                - bicycle_profile (str): either road, gravel, mtb. Is the type of byke
                - number_of_days (int): the number of days the trip will last
                - dates (list[date]): starting and ending date of the trip
                - places (list[Place]): list of places, the first is the starting point, the last is the ending point
                - selected_raw_route (int): index of the selected raw route, if None, no route was selected
        Raises:
            ValueError: if the given things dictionary contains an invalid key or an invalid value type
        Examples:
        ```python
        trip = TripDescriptor()
        trip.fill({
            "ride_type": "one_way",
            "bicycle_profile": "gravel",
            "number_of_days": 4,
            "dates": [date(2023, 10, 1), date(2023, 10, 5)],
            "places": ["Udine", "Palmanova", "Trieste"]
        })
        """
        for key in things.keys():
            if key == "ride_type":
                assert isinstance(things["ride_type"], str), f"in TripDescriptor.fill()\nThe given ride_type must be of type string\n{things['ride_type'].__class__} was provided"
                self.ride_type = things["ride_type"]

            elif key == "bicycle_profile":
                assert isinstance(things["bicycle_profile"], str), f"in TripDescriptor.fill()\nThe given bicycle_profile must be of type string\n{things['bicycle_profile'].__class__} was provided"
                assert things["bicycle_profile"] in ["road", "gravel", "mtb"], f"in TripDescriptor.fill()\nThe given bicycle_profile must be one of the following: road, gravel, mtb\n{things['bicycle_profile']} was provided"
                self.bicycle_profile = things["bicycle_profile"]
                
            elif key == "number_of_days":
                assert isinstance(things["number_of_days"], int), f"in TripDescriptor.fill()\nThe given number_of_days must be an of type integer\n{things['number_of_days'].__class__} was provided"
                assert things["number_of_days"] > 0, f"in TripDescriptor.fill()\nThe given number_of_days must be greater than 0\n{things['number_of_days']} was provided"
                self.number_of_days = things["number_of_days"]

            elif key == "dates":
                assert isinstance(things["dates"], list), f"in TripDescriptor.fill()\nThe given dates must be of type list\n{things['dates'].__class__} was provided"
                if len(things["dates"]) > 0 : assert isinstance(things["dates"][0], date), f"in TripDescriptor.fill()\nThe given dates elements must be of type date\n{things['dates'][0].__class__} was provided"
                self.dates = things["dates"]

            if key == "places":
                assert isinstance(things["places"], list), f"in RouteDescriptor.fill()\nThe given places must be of type list, list of place\n{things['places'].__class__} was provided"
                assert len(things["places"]) > 2, f""
                assert isinstance(things["places"][0], str), f"in RouteDescriptor.fill()\nThe given places element must be of type str\n{things['places'][0].__class__} was provided"
                self.places = [Place(name=plc) for plc in things["places"]]
                self.__plan_candidate_raw_routes()

            elif key == "selected_raw_route":
                assert isinstance(things["selected_raw_route"], int), f"in RouteDescriptor.fill()\nThe given selected_raw_route must be of type integer\n{things['selected_raw_route'].__class__} was provided"
                assert self.candidate_raw_routes is not None, f"in RouteDescriptor.fill()\nThe candidate_raw_routes must be filled before selecting a raw route, please fill the route descriptor with places first\n"
                assert 0 <= things["selected_raw_route"] < len(self.candidate_raw_routes), f"in RouteDescriptor.fill()\nThe given selected_raw_route must be between 0 and 3\n{things['selected_raw_route']} was provided"
                self.selected_raw_route = things["selected_raw_route"]
                self.__plan_steps()

            else:
                raise ValueError(f"in TripDescriptor.fill()\nAttribute {key} cannot be filled by the user, or it is not a valid attribute of the TripDescriptor class")

    def __get_route(self, idx: int) -> list[list[float]]:
        """Get a route that goes through the places provided"""
        import requests

        locations_coordinates = [place.get_coordinates() for place in self.places]
        route = []
        for i in range(1, len(locations_coordinates)):
            lonlats_string = f"{locations_coordinates[i-1][1]},{locations_coordinates[i-1][0]}|{locations_coordinates[i][1]},{locations_coordinates[i][0]}"
            url = f"http://localhost:17777/brouter?lonlats={lonlats_string}&profile={self.bicycle_profile}&alternativeidx={idx}&format=geojson"
            response = requests.get(url)

            if response.status_code == 200:
                route.extend(response.json()["features"][0]["geometry"]["coordinates"])
            else:
                print(f"In RouteDescriptor.__get_route\nInput: \n\tlocations_coordinates: {locations_coordinates}\nRequest returned with code: {response.status_code}")

        return route
    
    def __plan_candidate_raw_routes(self) -> list[list[list[float]]]:
        """Get 4 different routes that goes through the places provided"""
        routes = []
        for i in range(4):
            route = self.__get_route(i)
            if len(route) > 0:
                routes.append(route)
        return routes
    
    def __geopoint_distance(self, a: list[float], b: list[float]) -> float:
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
    
    def __plan_steps(self, max_distance: float = 10000.0) -> None:
        """Plan the steps of the route based on the maximum distance"""
        if self.candidate_raw_routes is None or len(self.candidate_raw_routes) == 0:
            raise Exception("Error in RouteDescriptor.__plan_steps()\nThe candidate_raw_routes is None, please fill the route descriptor with places first\n")

        if self.selected_raw_route is None or self.selected_raw_route < 0 or self.selected_raw_route >= len(self.candidate_raw_routes):
            raise Exception(f"Error in RouteDescriptor.__plan_steps()\nThe selected_raw_route is {self.selected_raw_route}, it must be between 0 and {len(self.candidate_raw_routes) - 1} (inclusive)\nPlease fill the route descriptor with a valid selected_raw_route first\n")
        
        self.stepped_route = []
        self.length = 0.0
        choosen_raw_route = self.candidate_raw_routes[self.selected_raw_route]
        current_step = [choosen_raw_route[0]]
        current_distance = 0.0
        
        # TODO : correct length calculation
        # correct the logic to handle correctly the last geopoint in the route
        for geopoint in choosen_raw_route[1:]:
            current_distance += self.__geopoint_distance(current_step[-1], geopoint)
            
            if current_distance < max_distance:
                current_step.append(geopoint)
            else:
                self.stepped_route.append(current_step)
                self.length += current_distance
                current_step = [self.stepped_route[-1][-1], geopoint]
                current_distance = self.__geopoint_distance(current_step[0], geopoint)

    def debug_dict(self) -> dict:
        """Return a dictionary with the class and value of each attribute for debugging purposes"""
        return {
            "ride_type": {"class": self.get_ride_type().__class__, "value": self.get_ride_type()},
            "bicycle_profile": {"class": self.get_bicycle_profile().__class__, "value": self.get_bicycle_profile()},
            "number_of_days": {"class": self.get_number_of_days().__class__, "value": self.get_number_of_days()},
            "dates": {"class": self.get_dates().__class__, "value": self.get_dates()},
            "places": {"class": self.get_places().__class__, "value": [place.get_name() for place in self.get_places()]},
            "candidate_raw_routes": {"class": self.get_candidate_raw_routes().__class__, "value": self.get_candidate_raw_routes()},
            "selected_raw_route": {"class": self.get_selected_raw_route().__class__, "value": self.get_selected_raw_route()},
            "stepped_route": {"class": self.get_stepped_route().__class__, "value": self.get_stepped_route()},
            "length": {"class": self.get_length().__class__, "value": self.get_length()}
        }
    