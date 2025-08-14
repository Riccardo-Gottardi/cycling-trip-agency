import math

class DistanceCalculation:
    @classmethod
    def fcc_distance(cls, a: list[float], b: list[float]) -> float:
        """Calculate the geographical distance (in meter) between two points using the Federal Communication Commission formula (for distances under 475 km)"""
        lat_a, lon_a, _ = a
        lat_b, lon_b, _ = b

        difference_in_lon = lon_a - lon_b
        difference_in_lat = lat_a - lat_b

        mean_latitude = (lat_a + lat_b) / 2

        K1 = 111.13209 - 0.56605 * math.cos(2 * mean_latitude) + 0.00120 * math.cos(4 * mean_latitude)
        K2 = 111.41513 * math.cos(mean_latitude) - 0.09455 * math.cos(3 * mean_latitude) + 0.00012 * math.cos(5 * mean_latitude)

        D = math.sqrt(math.pow(K1 * difference_in_lat, 2) + math.pow(K2 * difference_in_lon, 2))
        
        return D * 1000
    
    @classmethod
    def __euclidian_distance(cls, a: list[float], b: list[float]) -> float:
        """Calculate the elevation distance between two geographical points"""
        squared_distances_sum = 0

        for i in range(len(a)):
            squared_distances_sum += (a[i] - b[i])**2

        return math.sqrt(squared_distances_sum)