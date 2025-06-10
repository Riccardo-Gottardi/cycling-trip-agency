from pydantic import BaseModel, Field
from datetime import date, timedelta


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
        self.__set_coordinates()

    def __set_coordinates(self) -> None:
        import requests
        
        params = {
            "q": self.name,
            "format": "json"
        }
        headers = {
            "User-Agent": "cycling-trip-acency, Place class"  
        }
        url = f"https://nominatim.openstreetmap.org/search"

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        if response.json():
            json_response = response.json()[0]
            self.lat = float(json_response["lat"])
            self.lon = float(json_response["lon"])
        else:
            raise ValueError(f"Could not find coordinates for the place: {self.name}")

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
            "bicycle_profile": "gravel",
            "number_of_days": 4,
        })
        trip.fill({"places": ["Udine", "Palmanova", "Trieste"]})
        candidate_routes = trip.get_candidate_raw_routes()
        ...
        trip.fill({"selected_raw_route": 0})
        ```
    """
    bicycle_profile: str = Field(default="", description="either road, gravel, mtb. Is the type of byke")
    number_of_days: int | None = Field(default=None, description="the number of days the trip will last")
    dates: list[date] | None = Field(default=None, description="starting and ending date of the trip")
    places: list[Place] = Field(default=[], description="list of places, the first is the starting point, the last is the ending point")
    candidate_raw_routes: list[list[list[float]]] | None = Field(default=None, description="list of candidate raw routes, each route is a list of geopoints, each geopoint is a list of 3 coordinates (lat, lon, elv)")
    selected_raw_route: int | None = Field(default=None, description="index of the selected raw route, if None, no route was selected")
    stepped_route: list[list[list[float]]] | None = Field(default=None, description="division of the trip as segments, list of geographical positions")
    length: float | None = Field(default=None, description="length of the route in meters")
    
    def get_bicycle_profile(self) -> str:
        return self.bicycle_profile
    
    def get_number_of_days(self) -> int | None:
        return self.number_of_days
    
    def get_dates(self) -> list[date] | None:
        return self.dates
    
    def get_places(self) -> list[Place]:
        return self.places
    
    def get_candidate_raw_routes(self) -> list[list[list[float]]] | None:
        return self.candidate_raw_routes
    
    def get_selected_raw_route(self) -> int | None:
        return self.selected_raw_route
    
    def get_stepped_route(self) -> list[list[list[float]]] | None:
        return self.stepped_route
    
    def get_length(self) -> float | None:
        return self.length

    def get_description(self) -> str:
        """Get a description of the trip"""
        description = ""
        
        if self.bicycle_profile:
            description += f"Bicycle profile: {self.bicycle_profile}. "
        if self.number_of_days:
            description += f"Number of days: {self.number_of_days}. "
        if len(self.places) > 0: 
            description += f", from {self.places[0].get_name()} to {self.places[-1].get_name()}. "
        if self.dates:
            description += f" Dates: {self.dates[0]} to {self.dates[1]}. "
        if self.candidate_raw_routes:
            description += f" Number of candidate routes: {len(self.candidate_raw_routes)}. "
        if self.selected_raw_route:
            description += f" Selected route index: {self.selected_raw_route}. "
        if self.stepped_route:
            description += f" Number of steps in the route: {len(self.stepped_route)}. "
        if self.length:
            description += f" Total length of the route: {self.length} meters. "
        
        if description == "":
            description += "No trip information available."
        
        return description
    
    def __set_bicycle_profile(self, bicycle_profile: str) -> None:
        if not bicycle_profile in ["road", "gravel", "mtb"]: raise TypeError(f"in TripDescriptor.__set_bicycle_profile()\nThe given bicycle_profile must be one of the following: road, gravel, mtb\n{bicycle_profile} was provided")
        self.bicycle_profile = bicycle_profile

    def __set_number_of_days(self, number_of_days: int) -> None:
        if not number_of_days > 0: raise TypeError(f"in TripDescriptor.__set_number_of_days()\nThe given number_of_days must be greater than 0\n{number_of_days} was provided")
        self.number_of_days = number_of_days

    def __set_dates(self, dates: list[date]) -> None:
        if not len(dates) > 0: raise TypeError(f"in TripDescriptor.__set_dates()\nThe given dates must contain at least 1 element, the starting date of the trip\n{len(dates)} were provided")
        self.dates = dates
        
    def __set_places(self, places: list[str]) -> None:  
        if not len(places) > 2: raise TypeError(f"in TripDescriptor.__set_places()\nThe given places must contain at least 2 elements, the starting and ending point of the trip\n{len(places)} were provided")
        self.places = [Place(name=plc) for plc in places]

    def __set_selected_raw_route(self, selected_raw_route: int) -> None:
        if self.candidate_raw_routes is None: raise TypeError(f"in RouteDescriptor.__set_selected_route()\nBefore selecting one of the candidate routes they must be created, please fill the route descriptor with places first\n")
        if not 0 <= selected_raw_route < len(self.candidate_raw_routes): raise TypeError(f"in RouteDescriptor.__set_selected_route()\nThe given selected_raw_route must be between 0 and {len(self.candidate_raw_routes)}\n{selected_raw_route} was provided")
        self.selected_raw_route = selected_raw_route

    def fill(self, things: dict) -> None:
        """Fill the TripDescriptor with the given things
        Args:
            things (dict): dictionary with the attributes to fill the TripDescriptor with. Key is the attribute name, value is the attribute value. settable attributes are:
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
                "bicycle_profile": "gravel",
                "number_of_days": 4,
                "dates": [date(2023, 10, 1), date(2023, 10, 5)],
                "places": ["Udine", "Palmanova", "Trieste"]
            })
            ```
        """
        for key in things.keys():
            if key == "bicycle_profile":
                self.__set_bicycle_profile(things["bicycle_profile"])
                
            elif key == "number_of_days":
                self.__set_number_of_days(things["number_of_days"])
                self.__correct_eventual_inconsistentcy_between_dates_number_of_days()

            elif key == "dates":
                self.__set_dates(things["dates"])
                self.__correct_eventual_inconsistentcy_between_dates_number_of_days()

            if key == "places":
                self.__set_places(things["places"])
                self.plan_candidate_raw_routes()

            elif key == "selected_raw_route":
                self.__set_selected_raw_route(things["selected_raw_route"])
                self.__plan_steps()

            else:
                raise ValueError(f"in TripDescriptor.fill()\nAttribute {key} cannot be filled by the user, or it is not a valid attribute of the TripDescriptor class")

    def __correct_eventual_inconsistentcy_between_dates_number_of_days(self) -> None:
        if self.dates is not None and self.number_of_days is not None:
            if (self.dates[1] - self.dates[0]).days + 1 != self.number_of_days:
                self.dates[1] = self.dates[0] + timedelta(days=self.number_of_days - 1)

    def __plan_route(self, idx: int) -> list[list[float]]:
        """Get a route that goes through the places provided"""
        import requests

        locations_coordinates = [place.get_coordinates() for place in self.places]
        route = []
        for i in range(1, len(locations_coordinates)):
            lonlats_string = f"{locations_coordinates[i-1][1]},{locations_coordinates[i-1][0]}|{locations_coordinates[i][1]},{locations_coordinates[i][0]}"
            url = f"http://localhost:17777/brouter?lonlats={lonlats_string}&profile={self.bicycle_profile}&alternativeidx={idx}&format=geojson"
            response = requests.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                route.extend(response.json()["features"][0]["geometry"]["coordinates"])
            else:
                raise Exception(f"Error in RouteDescriptor.__plan_route()\nThe request to the BRouter API failed with status code {response.status_code}\nURL: {url}\nResponse: {response.text}")

        return route
    
    def plan_candidate_raw_routes(self) -> None:
        """Get 4 different routes that goes through the places provided"""
        if self.places is None or len(self.places) < 2:
            raise Exception("Error in RouteDescriptor.__plan_candidate_raw_routes()\nThe places are not set, please fill the route descriptor with places first\n")
        if self.bicycle_profile is None or self.bicycle_profile not in ["road", "gravel", "mtb"]:
            raise Exception("Error in RouteDescriptor.__plan_candidate_raw_routes()\nThe bicycle_profile is not set, please fill the route descriptor with a valid bicycle profile first\n")

        self.candidate_raw_routes = []
        route = []
        for i in range(4):
            route = self.__plan_route(i)
            if len(route) > 0:
                self.candidate_raw_routes.append(route)
    
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
