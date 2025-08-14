from pydantic import BaseModel


class Place(BaseModel):
    """Represent a place
    Args:
        name (str): name of the place, it can be a city, a street, a point of interest, etc.
        osm_name (str): name of the 
        lat (float | None): latitude of the place, if None, it will be set automatically
        lon (float | None): longitude of the place, if None, it will be set automatically
        elv (float | None): elevation of the place, if None, it will be set automatically

    Examples:
        ```python
        udine = Place(name="Udine")
        louis_pordenone = Place(name="Louis, Pordenone")
        ```
    """
    name: str
    osm_name: str = ""
    lat: float | None = None
    lon: float | None = None
    elv: float | None = None
    
    def model_post_init(self, __context__=None) -> None:
        self.__set_coordinates()

    def __set_coordinates(self) -> None | str:
        import requests
        
        params = {
            "q": self.name,
            "format": "json"
        }
        headers = {
            "User-Agent": "cycling-trip-acency, Place class"  
        }
        url = f"https://nominatim.openstreetmap.org/search"

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        if response.json():
            json_response = response.json()[0]
            self.osm_name = str(json_response["display_name"])
            self.lat = float(json_response["lat"])
            self.lon = float(json_response["lon"])

    def get_name(self) -> str:
        """Get the name of the place"""
        return self.osm_name
    
    def get_users_name(self) -> str:
        """get the user's name"""
        return self.name

    def get_coordinates(self) -> list[float]:
        """Get the coordinates of the place"""
        if self.lat is None or self.lon is None:
            return []
        return [self.lat, self.lon, self.elv] if self.elv is not None else [self.lat, self.lon, 0.0]