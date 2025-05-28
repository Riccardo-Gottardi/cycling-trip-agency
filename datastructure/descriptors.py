from pydantic import BaseModel, Field
from datetime import date


class PerformanceDescriptor(BaseModel):
    """Class to describe the performance (a measure of cycling performance) of an entity"""
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


class Place(BaseModel):
    """"""
    name: str
    lat: float
    lon: float
    elv: float


class TripDescriptor(BaseModel):
    """Class to describe a bycicle trip"""
    ride_type: str = Field(default="", description="either ONE_WAY or LOOP. Tell if the starting point is also the ending point, or not")
    bicycle_profile: str = Field(default="", description="either ROAD, GRAVEL, MTB. Is the type of byke")
    number_of_days: int = Field(default=0, description="the number of days the trip will last")
    dates: list[date] | None = Field(default=None, description="starting and ending date of the trip")
    locations: list[str] = Field(default=[], description="city/monument to visit during the trip")
    planned_steps: list[list[list[float]]] | None = Field(default=None, description="division of the trip as segments, list of geographical positions")
    preferences: list[str] | None = Field(default=None, description="additional preferences about the trip, used to customize it as the user may like")
    

    def get_ride_type(self) -> str:
        return self.ride_type
    
    def get_bicycle_profile(self) -> str:
        return self.bicycle_profile
    
    def get_number_of_days(self) -> int:
        return self.number_of_days
    
    def get_dates(self) -> list[date] | None:
        return self.dates
    
    def get_locations(self) -> list[str] | None:
        return self.locations
    
    def get_planned_steps(self) -> list[list[list[float]]] | None:
        return self.planned_steps
    
    def get_preferences(self) -> list[str] | None:
        return self.preferences

    def fill(self, things: dict):
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
            elif key == "locations":
                assert isinstance(things["locations"], list), f"in TripDescriptor.fill()\nThe given locations must be of type list\n{things['locations'].__class__} was provided"
                if len(things["locations"]) > 0 : assert isinstance(things["locations"][0], str), f"in TripDescriptor.fill()\nThe given locations elements must be of type string\n{things['locations'][0].__class__} was provided"
                self.locations = things["locations"]
            elif key == "planned_steps":
                assert isinstance(things["planned_steps"], list), f"in TripDescriptor.fill()\nThe given planned_steps must be of type list, list of segments\n{things['planned_steps'].__class__} was provided"
                if len(things["planned_steps"]) > 0 : assert isinstance(things["planned_steps"][0], list), f"in TripDescriptor.fill()\nThe given planned_steps elements must be of type list, list of geopoints(list of 3 coordinates)\n{things['planned_steps'][0].__class__} was provided"
                if len(things["planned_steps"][0]) > 0 : assert isinstance(things["planned_steps"][0][0], list), f"in TripDescriptor.fill()\nThe given planned_steps elements elements must be of type list, geopoints(list of 3 coordinates)\n{things['planned_steps'][0][0].__class__} was provided"
                if len(things["planned_steps"][0][0]) > 0 : assert isinstance(things["planned_steps"][0][0][0], float), f"in TripDescriptor.fill()\nThe given planned_steps elements elements elements must be of type float, coortinates of a geopoints(list of 3 coordinates)\n{things['planned_steps'][0][0][0].__class__} was provided"
                self.planned_steps = things["planned_steps"]
            elif key == "preferences":
                assert isinstance(things["preferences"], list), f"in TripDescriptor.fill()\nThe given preferences must be of type list\n{things['preferences'].__class__} was provided"
                if len(things["preferences"]) > 0 : assert isinstance(things["preferences"][0], str), f"in TripDescriptor.fill()\nThe given preferences elements must be of type string\n{things['preferences'][0].__class__} was provided"
                self.preferences = things["preferences"]
            else:
                print(f"Warning: {key}, unexisting key was used when filling the trip descriptor")

    def debug_dict(self) -> dict:
        return {
            "ride_type": {"class": self.get_ride_type().__class__, "value": self.get_ride_type()},
            "bicycle_profile": {"class": self.get_bicycle_profile().__class__, "value": self.get_bicycle_profile()},
            "number_of_days": {"class": self.get_number_of_days().__class__, "value": self.get_number_of_days()},
            "dates": {"class": self.get_dates().__class__, "value": self.get_dates()},
            "locations": {"class": self.get_locations().__class__, "value": self.get_locations()},
            "planned_steps": {"class": self.get_planned_steps().__class__, "value": self.get_planned_steps()},
            "preferences": {"class": self.get_preferences().__class__, "value": self.get_preferences()}
        }
    

class RouteDescriptor(BaseModel):
    coordinates: list[list[float]]
    length: float
    