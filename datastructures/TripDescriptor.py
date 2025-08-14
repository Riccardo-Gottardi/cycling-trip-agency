import math
from pydantic import BaseModel
from datetime import date, timedelta
from datastructures.Place import Place
from datastructures.DistanceCalculation import DistanceCalculation


class TripDescriptor(BaseModel):
    """Description of a bicycle trip
    Args:
        bike_type (str | None): either road, gravel, mtb. Is the type of byke
        places (list[Place] | None): list of places, the first is the starting point, the last is the ending point
        number_of_days (int | None): the number of days the trip will last
        dates (list[date] | None): starting and ending date of the trip
        candidate_routes (list[list[list[float]]] | None): list of candidate raw routes, each route is a list of geopoints, each geopoint is a list of 3 coordinates (lat, lon, elv)
        selected_route (int | None): index of the selected raw route
        stepped_route (list[list[list[float]]] | None): division of the trip as segments, list of geographical positions
        length (float | None): length of the route in meters

    Examples:
        ```python
        trip = TripDescriptor()
        trip.fill(
            bike_type = "gravel",
            number_of_days = 4,
        )
        trip.fill(places = ["Udine", "Palmanova", "Trieste"])
        candidate_routes = trip.get_candidate_routes()
        ...
        trip.fill(selected_route = 0)
        stepped_route = trip.get_stepped_route()
        ```
    """
    bike_type: str | None = None
    places: list[Place] | None = None
    number_of_days: int | None = None
    dates: list[date] | None = None
    candidate_routes: list[list[list[float]]] | None = None
    selected_route: int | None = None
    stepped_route: list[list[list[float]]] | None = None 
    length: float | None = None
    positive_height_difference: float | None = None
    
    def get_bike_type(self) -> str | None:
        return self.bike_type
    
    def get_places(self) -> list[Place] | None:
        return self.places

    def get_number_of_days(self) -> int | None:
        return self.number_of_days
    
    def get_dates(self) -> list[date] | None:
        return self.dates
    
    def get_candidate_routes(self) -> list[list[list[float]]] | None:
        return self.candidate_routes
    
    def get_selected_route(self) -> int | None:
        return self.selected_route

    def get_stepped_route(self) -> list[list[list[float]]] | None:
        return self.stepped_route
    
    def get_length(self) -> float | None:
        return self.length

    def get_positive_height_difference(self) -> float | None:
        return self.positive_height_difference

    def get_class_description(self) -> str:
        """Get a description of the class that represent the trip"""
        return """# TripDescriptor:
- bike_type: str | None = None
    - describe the type of bike used for the trip, either road, gravel of mtb
- places: list[Place] | None = None
    - collect the different places that trip have to go through
- number_of_days: int | None = None
    - the length in days of the trip
- dates: list[date] | None = None
    - the starting and ending date of the trip
- candidate_routes: list[list[list[float]]] | None = None
    - possible routes (based on places) to choose from
- selected_route: int | None = None
    - the index of the route choosen (among candidate_routes)
- stepped_route: list[list[list[float]]] | None = None
    - the final route divided in step
- length: float | None = None
    - the length of the trip
    - set automatically
- positive_height_difference: float | None = None
    - the positive height difference of the trip
    - set automatically
"""

    def get_description(self) -> str:
        """Get a description of the trip"""
        description = ""
        
        if self.bike_type:
            description += f"Bicycle profile: {self.bike_type}. "
        if self.number_of_days:
            description += f"Number of days: {self.number_of_days}. "
        if self.places and len(self.places) > 0: 
            description += f", from {self.places[0].get_name()} to {self.places[-1].get_name()}. "
        if self.dates:
            description += f" Dates: {self.dates[0]} to {self.dates[1]}. "
        if self.candidate_routes:
            description += f" Number of candidate routes: {len(self.candidate_routes)}. "
        if self.selected_route:
            description += f" Selected route index: {self.selected_route}. "
        if self.stepped_route:
            description += f" Number of steps in the route: {len(self.stepped_route)}. "
        if self.length:
            description += f" Total length of the route: {self.length} meters. "
        if self.positive_height_difference:
            description += f" Positive height difference: {self.positive_height_difference} meters. "

        if description == "":
            description += "No trip information available."
        
        return description
    
    def __set_bike_type(self, bike_type: str) -> None | str:
        if not bike_type in ["road", "gravel", "mtb"]: return f"Error in TripDescriptor.__set_bike_type()\nThe given bike_type must be one of BikeType type\n{bike_type} was provided"
        self.bike_type = bike_type

    def __set_places(self, places: list[str]) -> None | str:  
        if not len(places) > 1: return f"Error in TripDescriptor.__set_places()\nThe given places must contain at least 2 elements, the starting and ending point of the trip\n{len(places)} were provided"
        self.places = [Place(name=plc) for plc in places]

        not_found = ""
        for place in self.places:
            if place.get_name() == "":
                not_found += f"{place.get_users_name()}, "
        if not_found != "":
            return f"Error in TripDescriptor.__set_places()\nFor the following places were not found: {not_found}"

    def __set_number_of_days(self, number_of_days: int) -> None | str:
        if not number_of_days > 0: return f"Error in TripDescriptor.__set_number_of_days()\nThe given number_of_days must be greater than 0\n{number_of_days} was provided"
        self.number_of_days = number_of_days

    def __set_dates(self, dates: list[str]) -> None | str:
        if not len(dates) > 0: return f"Error in TripDescriptor.__set_dates()\nThe given dates must contain at least 1 element, the starting date of the trip\n{len(dates)} were provided"
        self.dates = [date.fromisoformat(d) for d in dates]

    def __set_selected_route(self, selected_route: int) -> None | str:
        if self.candidate_routes is None: return f"Error in RouteDescriptor.__set_selected_route()\nBefore selecting one of the candidate routes they must be created, please fill the route descriptor with places first\n"
        if not 0 <= selected_route < len(self.candidate_routes): return f"Error in RouteDescriptor.__set_selected_route()\nThe given selected_route must be between 0 and {len(self.candidate_routes)}\n{selected_route} was provided"
        self.selected_route = selected_route

    def fill(self, bike_type: None | str = None, places: None | list[str] = None, number_of_days: None | int = None, dates: None | list[str] = None, selected_route: None | int = None) -> None | str:
        """Fill the TripDescriptor with the given info
        Args:
            - bike_type (str) | None : is the type to bike, either road, gravel or mtb.
            - places (list[str]) | None : list of places, the first is the starting point, the last is the ending point
            - number_of_days (int) | None : the number of days the trip will last
            - dates (list[str]) | None : starting and ending date of the trip, formatted following iso 8601
            - selected_route (int) | None : index of the selected raw route

        Return:
            - None: if nothing went wrong
            - str: containing an error explanation if something went wrong

        Examples:
            ```python
            trip = TripDescriptor()
            trip.fill(
                bike_type = "gravel",
                number_of_days = 4,
                places = ["Udine", "Palmanova", "Trieste"],
            )
            ...
            trip.fill(dates = ["2023-10-1", "2023-10-5"])
            ```
        """
        if bike_type is not None:
            ret = self.__set_bike_type(bike_type) # pyright: ignore[reportArgumentType]
            if ret is not None:
                return ret

        if places is not None:
            ret = self.__set_places(places) # pyright: ignore[reportArgumentType]
            if ret is not None:
                return ret
            
        if number_of_days is not None:
            ret = self.__set_number_of_days(number_of_days) # pyright: ignore[reportArgumentType]
            if ret is not None:
                return ret
            ret = self.__correct_eventual_inconsistentcy_between_dates_number_of_days()
            if ret is not None:
                return ret

        if dates is not None:
            ret = self.__set_dates(dates) # pyright: ignore[reportArgumentType]
            if ret is not None:
                return ret
            ret = self.__correct_eventual_inconsistentcy_between_dates_number_of_days()
            if ret is not None:
                return ret

        if selected_route is not None:
            ret = self.__set_selected_route(selected_route) # pyright: ignore[reportArgumentType]
            if ret is not None:
                return ret

    def __correct_eventual_inconsistentcy_between_dates_number_of_days(self) -> None:
        if self.dates is not None and self.number_of_days is not None:
            if (self.dates[1] - self.dates[0]).days + 1 != self.number_of_days:
                self.dates[1] = self.dates[0] + timedelta(days=self.number_of_days - 1)

    def __plan_route(self, idx: int) -> list[list[float]]:
        """Get a route that goes through the places provided"""
        import requests

        bike_profile = self.bike_type
        if self.bike_type == "road":
            bike_profile = "fastbike"
        
        locations_coordinates = [place.get_coordinates() for place in self.places] # pyright: ignore[reportOptionalIterable]
        route = []
        for i in range(1, len(locations_coordinates)):
            lonlats_string = f"{locations_coordinates[i-1][1]},{locations_coordinates[i-1][0]}|{locations_coordinates[i][1]},{locations_coordinates[i][0]}"
            url = f"http://localhost:17777/brouter?lonlats={lonlats_string}&profile={bike_profile}&alternativeidx={idx}&format=geojson"
            response = requests.get(url)
            response.raise_for_status()

            route.extend(response.json()["features"][0]["geometry"]["coordinates"])

        return route
    
    def plan_candidate_routes(self) -> None | str:
        """Get 4 different routes that goes through the places provided"""
        if self.places is None or len(self.places) < 2:
            return "Error in RouteDescriptor.plan_candidate_routes()\nThe places are not set, please fill the route descriptor with places first\n"
        if self.bike_type is None or self.bike_type not in ["road", "gravel", "mtb"]:
            return "Error in RouteDescriptor.plan_candidate_routes()\nThe bike_type is not set, please fill the route descriptor with a valid bicycle profile first\n"

        self.candidate_routes = []
        route = []
        for i in range(4):
            route = self.__plan_route(i)
            if len(route) > 0:
                self.candidate_routes.append(route)
    
    def __check_consistency_number_of_days_number_of_steps(self) -> None | str:
        if not self.number_of_days:
            return 

        if not self.stepped_route:
            return "Error in RouteDescriptor.__check_consistency_number_of_days_number_of_steps()\nThe stepped_route is not set, please plan the stepped_route first\n"

        if len(self.stepped_route) > self.number_of_days:
            return "Error in RouteDescriptor.__check_consistency_number_of_days_number_of_steps()\nThe number of steps in the route is greater than the number of days\n"
    
    def plan_steps(self, max_distance: float = 40000.0, max_elevation: float = 500.0) -> None | str:
        """Plan the steps of the route based on the maximum distance"""
        if self.candidate_routes is None or len(self.candidate_routes) == 0:
            return "Error in RouteDescriptor.__plan_steps()\nThe candidate_routes is None, please fill the route descriptor with places first\n"

        if self.selected_route is None or self.selected_route < 0 or self.selected_route >= len(self.candidate_routes):
            return f"Error in RouteDescriptor.__plan_steps()\nThe selected_route is {self.selected_route}, it must be between 0 and {len(self.candidate_routes) - 1} (inclusive)\nPlease fill the route descriptor with a valid selected_route first\n"
        
        self.stepped_route = []
        self.length = 0.0
        self.positive_height_difference = 0.0
        choosen_raw_route = self.candidate_routes[self.selected_route]
        current_step = [choosen_raw_route[0]]
        lat_lon_distance = 0.0
        positive_height_difference = 0.0
        
        for geopoint in choosen_raw_route[1:]:
            lat_lon_distance_increment = DistanceCalculation.fcc_distance(current_step[-1], geopoint)
            height_increment = DistanceCalculation.eucledian_distance(current_step[-1], geopoint)

            if lat_lon_distance + lat_lon_distance_increment <= max_distance and positive_height_difference + height_increment <= max_elevation:
                current_step.append(geopoint)
                lat_lon_distance += lat_lon_distance_increment
                positive_height_difference += height_increment 
            else:
                self.stepped_route.append(current_step)
                self.length += lat_lon_distance
                self.positive_height_difference += positive_height_difference
                current_step = [self.stepped_route[-1][-1], geopoint]
                lat_lon_distance = lat_lon_distance_increment
                positive_height_difference = height_increment
        
        if self.stepped_route != []:
            if current_step != self.stepped_route[-1]:
                self.stepped_route.append(current_step)
        else:
            self.stepped_route.append(current_step)

        ret = self.__check_consistency_number_of_days_number_of_steps()
        if ret is not None:
            return ret
