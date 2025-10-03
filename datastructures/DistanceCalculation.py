import math

# TODO move this calss into a folder called utility
# it is a class but it doesn't hold any information
# there fore it should not be in the datastructure folder

class DistanceCalculation:
    @classmethod
    def fcc_distance(cls, a: list[float], b: list[float]) -> float:
        """Calculate the geographical distance (in meter) between two points using the Federal Communication Commission formula (for distances under 475 km)"""
        lat_a, lon_a, _ = a
        lat_b, lon_b, _ = b

        difference_in_lat = lat_a - lat_b
        difference_in_lon = lon_a - lon_b

        mean_latitude = (math.radians(lat_a) + math.radians(lat_b)) / 2

        k1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
        k2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

        d = math.sqrt(math.pow(k1 * difference_in_lat, 2) + math.pow(k2 * difference_in_lon, 2))
        
        return d * 1000
    
    @classmethod
    def euclidean_distance(cls, a: list[float], b: list[float]) -> float:
        """Calculate the Euclidean distance between two geographical points"""
        squared_distances_sum = 0

        for i in range(len(a)):
            squared_distances_sum += (a[i] - b[i])**2

        return math.sqrt(squared_distances_sum)

    @classmethod
    def positive_elevation_distance(cls, a: list[float], b: list[float]) -> float:
        """Calculate the positive elevation distance between two geographical points"""
        if a[2] < b[2]:
            return abs(a[2] - b[2])
        else:
            return 0.0