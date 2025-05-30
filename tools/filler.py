from pydantic_ai import RunContext
from datastructures.descriptors import TripDescriptor, PerformanceDescriptor, PreferencesDescriptor
from datastructures.dependencies import MyDeps


def fill_trip_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the trip description
    Args:
        gathered_informations (dict): contain the collected informations about the trip. They are structured as a dictionary, with as key the name of the field of the trip descriptor and as values the information/s to put in the trip descriptor.
    Returns:
        Nothing
    Examples:
        ```python
        fill_trip_descriptor({ride_type: "ONE_WAY", bicycle_profile: "GRAVEL"})
        fill_trip_descriptor({locations: ["Pordenone", "Palmanova", "Trieste"], number_of_days: 4})
        ```
    """
    assert isinstance(ctx.deps.trip, TripDescriptor), "In fill_trip_description\nAgent context deps.trip should be of type TripDescriptor"
    ctx.deps.trip.fill(gathered_informations)

def fill_user_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the performance description
    Args:
        gathered_informations (dict): contain the collected informations about the performance of the user. They are structured as a dictionary, with as key the name of the field of the performance descriptor and as values the information/s to put in the performance descriptor.
    Returns:
        Nothing
    Examples:
        ```python
        fill_user_description({preferences: {amenity: ["restaurant", "pub"], natural: ["coastline", "beach"]}, performance: {kilometer_per_day: 100}})
        fill_user_description({performance: {difference_in_height_per_day: 100, kilomenter_per_day: 40}})
        ```
    """
    assert isinstance(ctx.deps.user, PerformanceDescriptor), "In fill_performance_description\nAgent context deps.performance should be of type PerformanceDescriptor"
    ctx.deps.user.fill(gathered_informations)

def fill_performance_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the performance description
    Args:
        gathered_informations (dict): contain the collected informations about the performance of the user. They are structured as a dictionary, with as key the name of the field of the performance descriptor and as values the information/s to put in the performance descriptor.
    Returns:
        Nothing
    Examples:
        ```python
        fill_performance_description({kilometer_per_day: 100})
        fill_performance_description({difference_in_height_per_day: 100, kilomenter_per_day: 40})
        ```
    """
    assert isinstance(ctx.deps.user.performance, PerformanceDescriptor), "In fill_performance_description\nAgent context deps.performance should be of type PerformanceDescriptor"
    ctx.deps.user.performance.fill(gathered_informations)

def fill_preferences_description(ctx: RunContext[MyDeps], gathered_informations: dict):
    """A tool to fill the preferences description
    Args:
        gathered_informations (dict): contain the collected informations about the preferences for pois of the user. They are structured as a dictionary, with as key the name of the field of the preference descriptor and as values the information/s to put in the preference descriptor.
    Returns:
        Nothing
    Examples:
        ```python
        fill_preferences_description({amenity: [monument], natural: [], whater: ["lake"]})
        fill_preferences_description({difference_in_height_per_day: 100, kilomenter_per_day: 40})
        ```
    """
    assert isinstance(ctx.deps.user.preferences, PreferencesDescriptor), "In fill_performance_description\nAgent context deps.performance should be of type PerformanceDescriptor"
    ctx.deps.user.performance.fill(gathered_informations)