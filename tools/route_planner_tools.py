from datetime import date
from enum import Enum

from pydantic_ai import RunContext

from datastructures.dependencies import MyDeps
from datastructures.TripDescriptor import Place


class TripInfo(Enum): 
    BIKE_TYPE = "bike_type"
    PLACES = "places"
    NUMBER_OF_DAYS = "number_of_days"
    DATES = "dates"
    CANDIDATE_ROUTES = "candidate_routes"
    SELECTED_ROUTE = "selected_route"
    STEPPED_ROUTE = "stepped_route"
    LENGTH = "length"

class UserInfo(Enum):
    class Preference(Enum):
        AMENITY = "amenity"
        TOURISM = "tourism"
        HISTORIC = "historic"
        BUILDING = "building"
        NATURAL = "natural"
        WATER = "water"
        LEISURE = "leisure"
        MAN_MADE = "man_made"

    class Performance(Enum):
        KILOMETER_PER_DAY = "kilometer_per_day"
        POSITIVE_HEIGHT_DIFFERENCE_PER_DAY = "positive_height_difference_per_day"


def say_to_the_user(question: str) -> str:
    """Ask a question to the user and return the answer.
    Args:
        question (str): The question to ask the user.
    Returns:
        str: The user's answer.
    Examples:
        ```python
        answer = say_to_the_user("What is your favorite color?")
        ```
    """
    return input(f"{question}\n")

def get_trip_information(ctx: RunContext[MyDeps], trip_info: TripInfo) -> str | list[Place] | int | list[date] | list[list[list[float]]] | float | None:
    """A tool to get an information about the trip.
    Args:
        trip_info (TripInfo): The type of trip information to retrieve.
    Returns:
        - str | list[Place] | int | list[date] | list[list[list[float]]] | float: The requested trip information.
        - None: If the requested trip information is not available or was not set yet.
    Examples:
        ```python
        bike_type = get_trip_information(ctx, TripInfo.BIKE_TYPE)
        places = get_trip_information(ctx, TripInfo.PLACES)
        ```
    """
    match trip_info:
        case TripInfo.BIKE_TYPE:
            return ctx.deps.trip.get_bike_type()
        case TripInfo.PLACES:
            return ctx.deps.trip.get_places()
        case TripInfo.NUMBER_OF_DAYS:
            return ctx.deps.trip.get_number_of_days()
        case TripInfo.DATES:
            return ctx.deps.trip.get_dates()
        case TripInfo.CANDIDATE_ROUTES:
            return ctx.deps.trip.get_candidate_routes()
        case TripInfo.SELECTED_ROUTE:
            return ctx.deps.trip.get_selected_route()
        case TripInfo.STEPPED_ROUTE:
            return ctx.deps.trip.get_stepped_route()
        case TripInfo.LENGTH:
            return ctx.deps.trip.get_length()
        
def get_user_information(ctx: RunContext[MyDeps], user_info: UserInfo):
    """A tool to get an information about the user.
    Args:
        user_info (UserInfo): The type of user information to retrieve.
    Returns:
        - str | None: The requested user information.
        - None: If the requested user information is not available or was not set yet.
    Examples:
        ```python
        amenity_preferences = get_user_information(ctx, UserInfo.Preference.AMENITY)
        kilomenter_per_day = get_user_information(ctx, UserInfo.Performance.KILOMETER_PER_DAY)
        ```
    """
    match user_info:
        case UserInfo.Preference.AMENITY:
            return ctx.deps.user.get_preferences().get_amenity()
        case UserInfo.Preference.TOURISM:
            return ctx.deps.user.get_preferences().get_tourism()
        case UserInfo.Preference.HISTORIC:
            return ctx.deps.user.get_preferences().get_historic()
        case UserInfo.Preference.BUILDING:
            return ctx.deps.user.get_preferences().get_building()
        case UserInfo.Preference.NATURAL:
            return ctx.deps.user.get_preferences().get_natural()
        case UserInfo.Preference.WATER:
            return ctx.deps.user.get_preferences().get_water()
        case UserInfo.Preference.LEISURE:
            return ctx.deps.user.get_preferences().get_leisure()
        case UserInfo.Preference.MAN_MADE:
            return ctx.deps.user.get_preferences().get_man_made()
        case UserInfo.Performance.KILOMETER_PER_DAY:
            return ctx.deps.user.get_performance().get_kilometer_per_day()
        case UserInfo.Performance.POSITIVE_HEIGHT_DIFFERENCE_PER_DAY:
            return ctx.deps.user.get_performance().get_positive_height_difference_per_day

def plan_the_candidate_routes(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to plan the candidate routes for the trip.
    Returns:
        - str: an error message if something went wrong.
        - None: if everything went right.
    """
    return ctx.deps.trip.plan_candidate_routes()

def plan_the_route_steps(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to plan the steps for the selected route.
    Returns:
        - str: an error message if something went wrong.
        - None: if everything went right.
    """
    return ctx.deps.trip.plan_steps(max_distance=ctx.deps.user.get_performance().get_kilometer_per_day(), max_elevation=ctx.deps.user.get_performance().get_positive_height_difference_per_day())

def get_route_recommendation() -> str:
    """A tool to add point of interest to the route.
    Returns:
        - string containing output of the agent
    Examples:
        ```python
        get_route_recommendation()
        ```
    """
    return "This is a placeholder for the route recommendation logic."