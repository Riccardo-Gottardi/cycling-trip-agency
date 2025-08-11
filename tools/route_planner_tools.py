from datetime import date

from pydantic_ai import RunContext

from datastructures.dependencies import MyDeps
from datastructures.TripDescriptor import Place

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


def get_route_recommendation() -> str:
    """A tool to add point of intereset to the route.
    Returns:
        - string containing output of the agent
    Examples:
        ```python
        recommender_agent()
        ```
    """
    return "This is a placeholder for the route recommendation logic."


def get_trip_information(ctx: RunContext[MyDeps], bike_type: bool = False, places: bool = False, number_of_days: bool = False, dates: bool = False, candidate_raw_routes: bool = False, selected_raw_route: bool = False, stepped_route: bool = False, length: bool = False) -> str | list[Place] | int | list[date] | list[list[list[float]]] | float | None:
    """A tool to get an information about the trip.
    Args:
        - bike_type (bool): Whether to get bike type information.
        - places (bool): Whether to get places information.
        - number_of_days (bool): Whether to get number of days information.
        - dates (bool): Whether to get dates information.
        - candidate_raw_routes (bool): Whether to get candidate raw routes information.
        - selected_raw_route (bool): Whether to get selected raw route information.
        - stepped_route (bool): Whether to get stepped route information.
        - length (bool): Whether to get length information.
    Return:
        - str | list[Place] | int | list[date] | list[list[list[float]]] | float | None: The requested trip information.
    Examples:
        ```python
        bike_type = get_trip_information(ctx, bike_type=True)
        places = get_trip_information(ctx, places=True)
        ```
    Note:
        - This function will return None if no information is requested.
        - This function return only one piece of information at a time.
    """
    if bike_type:
        return ctx.deps.trip.get_bike_type()
    elif places:
        return ctx.deps.trip.get_places()
    elif number_of_days:
        return ctx.deps.trip.get_number_of_days()
    elif dates:
        return ctx.deps.trip.get_dates()
    elif candidate_raw_routes:
        return ctx.deps.trip.get_candidate_raw_routes()
    elif selected_raw_route:
        return ctx.deps.trip.get_selected_raw_route()
    elif stepped_route:
        return ctx.deps.trip.get_stepped_route()
    elif length:
        return ctx.deps.trip.get_length()