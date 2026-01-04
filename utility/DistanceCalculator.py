from datastructures.Place import Place
from utility.distance_calculation import fcc_distance

class DistanceCalculator:
    places: dict[str, Place] = {}

    @classmethod
    def approximate_itinerary_length(cls, itinerary: list[str]) -> int:
        """Given a collection of places, that made up the itinerary, it calculate the total length of the itinerary
        Args:
            itinerary (list[str]): list of the names of the places that made up the itinerary. For more precise results, use the full name (e.g. "City, Country")
        Returns:
            int: the approximate length of the itinerary in meters
        Raises:
            Exception: if a place is not found or other error occurs
        Example:
            ```python
            i_length = DistanceCalculator.approximate_itinerary_length(["Trieste, Italy", "Monfalcone, Italy", "Gemona, Italy"])
            ```
        """
        tmp = []
        for p in itinerary:
            if p in cls.places:
                tmp.append(cls.places[p].get_coordinates())
            else:
                try:
                    place = Place(name=p)
                    cls.places[p] = place
                    tmp.append(place.get_coordinates())
                except Exception as e:
                    raise e

        d = 0

        for i in range(1, len(tmp)):
            d += fcc_distance(tmp[i-1], tmp[i])

        return int(d)
