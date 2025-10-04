from datastructures.Place import Place
from utility.distance_calculation import fcc_distance
from datastructures.FinalResults import Itinerary


def approximate_itinerary_length(places: list[str]):
    """Given a collection of places, that made up the itinerary, it calculate the total length of the itinerary
    Args:
        places (list[str]): list of the names of the places that made up the itinerary 
    Returns:
        int: the approximate length of the itinerary in meters
    Raises:
        Exception: if a place is not found or other error occurs
    Example:
        ```python
        approximate_itinerary_length(["Trieste", "Gemona", "Udine"])
        ```
    """
    try:
        tmp = [Place(name=p) for p in places]
    except Exception as e:
        return str(e)

    d = 0

    for i in range(1, len(tmp)):
        d += fcc_distance(tmp[i-1].get_coordinates(), tmp[i].get_coordinates())

    return d