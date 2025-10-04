from pydantic_ai import RunContext
from datastructures.MyDeps import MyDeps
from datastructures.Place import Place
from utility.distance_calculation import fcc_distance


def approximate_segment_length(places: list[str]):
    """Given a collection of places, that made up the segment, it calculate the total length of the segment
    Args:
        places (list[str]): list of the names of the places that made up the segment
    Returns:
        int: the approximate length of the segment in meters
    Raises:
        Exception: if a place is not found or other error occurs
    Example:
        ```python
        approximate_segment_length(["Trieste", "Monfalcone", "Gemona"])
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

def generate_gpx_route(ctx: RunContext[MyDeps]):
    """Generates a GPX route based on the trip description in deps.
    Example:
        ```python
        generate_gpx_route()
        ```
    """
    ctx.deps.trip.generate_gpx_route()