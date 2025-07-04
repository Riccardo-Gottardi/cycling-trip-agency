from pydantic_ai import RunContext
from datastructures.dependencies import MyDeps


def fill_trip_description(ctx: RunContext[MyDeps], bike_type: None | str = None, places: None | list[str] = None, number_of_days: None | int = None, dates: None | list[str] = None, selected_raw_route: None | int = None) -> None | str:
    """A tool to fill the trip description
    Args:
        - bike_type (str) : is the type to bike, either road, gravel or mtb.
        - places (list[str]) : list of places, the first is the starting point, the last is the ending point
        - number_of_days (int) : the number of days the trip will last
        - dates (list[str]) : starting and ending date of the trip, formatted following iso 8601
        - selected_raw_route (int) : index of the selected raw route

    Return:
        - None: if nothing went wrong
        - str: containing an error explanation if something went wrong
    
    Examples:
        ```python
        fill_trip_descriptor(bike_type="gravel")
        fill_trip_descriptor(places=["Pordenone", "Palmanova"], number_of_days=4)
        ```
    """
    ret = ctx.deps.trip.fill(bike_type, places, number_of_days, dates, selected_raw_route)
    if ret != None:
        return ret

def fill_user_description(ctx: RunContext[MyDeps], preferences: dict | None = None, performance: dict | None = None) -> None | str:
    """A tool to fill the performance description
    Args:
        - preferences (dict) : a dictionary containing the preferences of the user, with keys like amenity and natural, and values being lists of strings
        - performance (dict) : a dictionary containing the performance of the user, with keys like kilometer_per_day and difference_in_height_per_day, and values being integers
    Returns:
        Nothing
    Examples:
        ```python
        fill_user_description(preferences = {amenity: ["restaurant", "pub"], natural: ["coastline", "beach"]}, performance = {kilometer_per_day: 100})
        fill_user_description(performance = {difference_in_height_per_day: 100, kilometer_per_day: 40})
        ```
    """
    res = ctx.deps.user.fill(preferences, performance)
    if res != None:
        return res