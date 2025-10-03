from datastructures.Place import Place
from datastructures.DistanceCalculation import DistanceCalculation
from datastructures.FinalResults import PlannerFinalResult


def approximate_itinerary_distance(places: list[str]):
    """Given a collection of places, that made up the itinerary, it calculate the total length of the itinerary
    Args:
        places (list[str]): list of the names of the places that made up the itinerary 
    Returns:
        int: the approximate length of the itinerary in meters
    Raises:
        Exception: if a place is not found or other error occurs
    Example:
        ```python
        approximate_itinerary_distance(["Trieste", "Gemona", "Udine"])
        ```
    """
    try:
        tmp = [Place(name=p) for p in places]
    except Exception as e:
        return str(e)

    d = 0

    for i in range(1, len(tmp)):
        d += DistanceCalculation.fcc_distance(tmp[i-1].get_coordinates(), tmp[i].get_coordinates())

    return d