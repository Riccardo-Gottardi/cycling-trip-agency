from datetime import date
from enum import Enum

from pydantic_ai import RunContext

from datastructures.dependencies import MyDeps
from datastructures.TripDescriptor import Place


# TODO  Make the tools used by the agent handle exceptions
#       They catch the exceptions and return a user-friendly error message.

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

def get_trip_information(ctx: RunContext[MyDeps], trip_info: str) -> str | None:
    """A tool to get an information about the trip.
    Args:
        trip_info (str): The name of the trip information to retrieve from the TripDescriptor.
    Returns:
        - str: The requested trip information.
        - None: If the requested trip information is not available or was not set yet.
    Examples:
        ```python
        bike_type = get_trip_information("bike_type")
        places = get_trip_information("places")
        ```
    """
    match trip_info:
        case "bike_type":
            return ctx.deps.trip.get_bike_type()
        case "places":
            return str(ctx.deps.trip.get_places())
        case "number_of_days":
            return str(ctx.deps.trip.get_number_of_days())
        case "dates":
            return str(ctx.deps.trip.get_dates())
        case "candidate_routes":
            return str(ctx.deps.trip.get_candidate_routes())
        case "selected_route":
            return str(ctx.deps.trip.get_selected_route())
        case "stepped_route":
            return str(ctx.deps.trip.get_stepped_route())
        case "length":
            return str(ctx.deps.trip.get_length())
        case "positive_height_difference":
            return str(ctx.deps.trip.get_positive_height_difference())

def get_user_information(ctx: RunContext[MyDeps], user_info: str) -> str | None:
    """A tool to get an information about the user.
    Args:
        user_info (str): The name of the user information to retrieve from the UserDescriptor.
    Returns:
        - str: The requested user information.
        - None: If the requested user information is not available or was not set yet.
    Examples:
        ```python
        amenity_preferences = get_user_information("amenity")
        kilomenter_per_day = get_user_information("kilometer_per_day")
        ```
    """
    match user_info:
        case "amenity":
            return str(ctx.deps.user.get_preferences().get_amenity())
        case "tourism":
            return str(ctx.deps.user.get_preferences().get_tourism())
        case "historic":
            return str(ctx.deps.user.get_preferences().get_historic())
        case "building":
            return str(ctx.deps.user.get_preferences().get_building())
        case "natural":
            return str(ctx.deps.user.get_preferences().get_natural())
        case "water":
            return str(ctx.deps.user.get_preferences().get_water())
        case "leisure":
            return str(ctx.deps.user.get_preferences().get_leisure())
        case "man_made":
            return str(ctx.deps.user.get_preferences().get_man_made())
        case "kilometer_per_day":
            return str(ctx.deps.user.get_performance().get_kilometer_per_day())
        case "positive_height_difference_per_day":
            return str(ctx.deps.user.get_performance().get_positive_height_difference_per_day())
        case "additional_note":
            return str(ctx.deps.user.get_additional_note())
        
def get_recommendations(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to get the founded recommendations for the trip.
    Returns:
        - str: the recommendations for the trip.
        - None: if no recommendations were found or the user preferences were not set.
    Examples:
        ```python
        recommendations = get_recommendations()
        ```
    """
    recommendations = ctx.deps.recommendation.get_recommended_places()
    if recommendations is not None or len(recommendations) > 0:
        return "".join(f"{r}\n" for r in recommendations)

def generate_the_candidate_routes(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to plan the candidate routes for the trip.
    Returns:
        - str: an error message if something went wrong.
        - None: if everything went right.
    Examples:
        ```python
        error = generate_the_candidate_routes()
        ```
    """
    return ctx.deps.trip.plan_candidate_routes()

def divide_the_route_in_steps(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to plan the steps for the selected route.
    Returns:
        - str: an error message if something went wrong.
        - None: if everything went right.
    Examples:
        ```python
        error = divide_the_route_in_steps()
        ```
    """
    return ctx.deps.trip.plan_steps(max_distance=ctx.deps.user.get_performance().get_kilometer_per_day(), max_elevation=ctx.deps.user.get_performance().get_positive_height_difference_per_day())

def find_the_recommendations(ctx: RunContext[MyDeps]) -> str | None:
    """A tool to plan the recommendations for the trip.
    Returns:
        - str: an error message if something went wrong.
        - None: if everything went right.
    Examples:
        ```python
        error = find_the_recommendations()
        ```
    """
    candidate_routes = ctx.deps.trip.get_candidate_routes()
    selected_route = ctx.deps.trip.get_selected_route()
    amenityes = ctx.deps.user.get_preferences().get_amenity()
    
    if candidate_routes and selected_route and amenityes:
        route = candidate_routes[selected_route]

        ctx.deps.recommendation.find_route_recommendations(route, amenityes)
    else:
        return "No candidate routes or selected route found."
