from utility.DistanceCalculator import DistanceCalculator


def approximate_segment_length(segment: list[str]):
    """Given a collection of places, that made up the segment, it calculate the total length of the segment
    Args:
        segment (list[str]): list of the names of the places that made up the segment. For more precise results, use the full name (e.g. "City, Country")
    Returns:
        int: the approximate length of the segment in meters
    Raises:
        Exception: if a place is not found or other error occurs
    Example:
        ```python
        s_length = approximate_segment_length(["Trieste, Italy", "Monfalcone, Italy", "Gemona, Italy"])
        ```
    """
    d = 0
    try:
        d = DistanceCalculator.approximate_itinerary_length(segment)
    except Exception as e:
        return str(e)

    return d