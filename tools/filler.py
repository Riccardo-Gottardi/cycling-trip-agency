from pydantic_ai import RunContext
from datastructures.dependencies import MyDeps


def fill_trip_description(ctx: RunContext[MyDeps], bike_type: None | str = None, places: None | list[str] = None, number_of_days: None | int = None, dates: None | list[str] = None, selected_route: None | int = None) -> None | str:
    """A tool to fill the trip description
    Args:
        - bike_type (str) : is the type to bike, either road, gravel or mtb.
        - places (list[str]) : list of places, the first is the starting point, the last is the ending point
        - number_of_days (int) : the number of days the trip will last
        - dates (list[str]) : starting and ending date of the trip, formatted following iso 8601
        - selected_route (int) : index of the selected raw route

    Return:
        - None: if nothing went wrong
        - str: containing an error explanation if something went wrong
    
    Examples:
        ```python
        fill_trip_description(bike_type="gravel")
        fill_trip_description(places=["Pordenone", "Palmanova"], number_of_days=4)
        ```
    """
    try:
        ctx.deps.trip.fill(bike_type, places, number_of_days, dates, selected_route)
    except Exception as e:
        return str(e)

def fill_user_preferences_deprecated(ctx: RunContext[MyDeps], amenity: None | dict = None, tourism: None | dict = None, natural: None | dict = None, historic: None | dict = None, building: None | dict = None, water: None | dict = None, leisure: None | dict = None, man_made: None | dict = None) -> None | str:
    """A tool to fill the preferences description
    Args:
        - amenity (dict) : a dictionary containing the amenity preferences of the user
        - tourism (dict) : a dictionary containing the tourism preferences of the user
        - natural (dict) : a dictionary containing the natural preferences of the user
        - historic (dict) : a dictionary containing the historic preferences of the user
        - building (dict) : a dictionary containing the building preferences of the user
        - water (dict) : a dictionary containing the water preferences of the user
        - leisure (dict) : a dictionary containing the leisure preferences of the user
        - man_made (dict) : a dictionary containing the man-made preferences of the user
    Examples:
        ```python
        fill_user_preferences(amenity = {"restaurant": ["Italian", "Chinese"]}, tourism = {"museums": ["Louvre"]}, natural = {"coastline": ["beach"]}, historic = {"castles": ["Neuschwanstein"]}, building = {"skyscrapers": ["Burj Khalifa"]}, leisure = {"parks": ["Central Park"]}, man_made = {"bridges": ["Golden Gate Bridge"]})
        ```
    """
    try:
        ctx.deps.user.preferences.fill(amenity, tourism, natural, historic, building, leisure, man_made)
    except Exception as e:
        return str(e)
    
def fill_user_preferences(ctx: RunContext[MyDeps], category: str, preference_type: str, preference_detail: list[str]) -> None | str:
    """A tool to fill the user preferences
    Args:
        - category (str) : the category of the preference, e.g. "amenity", "tourism", etc.
        - preference_type (str) : the type of the preference, e.g. "restaurant", "museums", etc.
        - preference_detail (list[str]) : a list of details for the preference, e.g. ["Italian", "Chinese"]
    Examples:
        ```python
        fill_user_preferences(category="amenity", preference_type="restaurant", preference_detail=["Italian", "Chinese"])
        ```
    """
    try:
        ctx.deps.user.preferences.add_preference(category, preference_type, preference_detail)
    except Exception as e:
        return str(e)

def fill_user_performance(ctx: RunContext[MyDeps], kilometre_per_day: None | int = None, positive_height_difference_per_day: None | int = None) -> None | str:
    """A tool to fill the performance description
    Args:
        - kilometre_per_day (int) : the number of kilometres the user can ride per day
        - positive_height_difference_per_day (int) : the positive height difference the user can handle per day
    Examples:
        ```python
        fill_user_performance(kilometre_per_day=100)
        fill_user_performance(positive_height_difference_per_day=100, kilometre_per_day=40)
        ```
    """
    try:
        ctx.deps.user.performance.fill(kilometre_per_day, positive_height_difference_per_day)
    except Exception as e:
        return str(e)
    
def fill_user_additional_note(ctx: RunContext[MyDeps], additional_note: str) -> None | str:
    """A tool to fill the additional note description
    Args:
        - additional_note (str) : the additional note about the user
    Examples:
        ```python
        fill_user_additional_note(additional_note="User prefers scenic routes")
        ```
    """
    res = ctx.deps.user.set_additional_note(additional_note)
    if res is not None:
        return res