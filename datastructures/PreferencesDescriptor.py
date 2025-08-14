from pydantic import BaseModel


class  PreferencesDescriptor(BaseModel):
    """Preference of the user for the points of interest"""
    possible_amenity: set[str] = {"restaurant", "cafe", "bar", "fast_food", "pub", "tourist_information", "place_of_worship", "parking", "toilets", "bench", "drinking_water", "bicycle_parking", "bicycle_rental", "bicycle_repair_station"}
    possible_tourism: set[str] = {"museum", "gallery", "viewpoint", "zoo", "aquarium", "theme_park", "information", "attraction"}
    possible_historic: set[str] = {"monument", "memorial", "castle", "ruins", "archaeological_site", "fort", "wayside_cross", "wayside_shrine", "battlefield", "church", "cathedral", "mosque", "synagogue", "temple", "tower"}
    possible_building: set[str] = {"cathedral", "palace", "castle", "church", "mosque", "synagogue", "temple"}
    possible_natural: set[str] = {"water", "peak", "volcano", "coastline", "beach", "cave_entrance", "waterfall", "spring", "glacier", "wood", "forest", "wetland"}
    possible_water: set[str] = {"lake", "river", "pond", "reservoir", "canal"}
    possible_leisure: set[str] = {"park", "garden", "nature_reserve", "playground", "resort", "golf_course", "stadium"}
    possible_man_made: set[str] = {"lighthouse", "bridge", "obelisk", "tower"}
    amenity: dict | None = None
    tourism: dict | None = None
    historic: dict | None = None
    building: dict | None = None
    natural: dict | None = None
    water: dict | None = None
    leisure: dict | None = None
    man_made: dict | None = None

    def get_amenity(self) -> dict | None:
        return self.amenity

    def get_tourism(self) -> dict | None:
        return self.tourism

    def get_historic(self) -> dict | None:
        return self.historic

    def get_building(self) -> dict | None:
        return self.building

    def get_natural(self) -> dict | None:
        return self.natural

    def get_water(self) -> dict | None:
        return self.water

    def get_leisure(self) -> dict | None:
        return self.leisure

    def get_man_made(self) -> dict | None:
        return self.man_made
    
    def get_class_description(self) -> str:
        """Get a string description of the class"""
        return f"""## PreferencesDescriptor:
- amenity: dict | None = None
    - the list of amenities the user prefers
    - can be one or more of the following: {', '.join(self.possible_amenity)}
- tourism: dict | None = None
    - the list of tourism points the user prefers
    - can be one or more of the following: {', '.join(self.possible_tourism)}
- historic: dict | None = None
    - the list of historic points the user prefers
    - can be one or more of the following: {', '.join(self.possible_historic)}
- building: dict | None = None
    - the list of buildings the user prefers
    - can be one or more of the following: {', '.join(self.possible_building)}
- natural: dict | None = None
    - the list of natural points the user prefers
    - can be one or more of the following: {', '.join(self.possible_natural)}
- water: dict | None = None
    - the list of water points the user prefers
    - can be one or more of the following: {', '.join(self.possible_water)}
- leisure: dict | None = None
    - the list of leisure points the user prefers
    - can be one or more of the following: {', '.join(self.possible_leisure)}
- man_made: dict | None = None
    - the list of man-made points the user prefers
    - can be one or more of the following: {', '.join(self.possible_man_made)}
"""

    def get_description(self) -> str:
        description = ""

        if self.amenity:
            description += f"Amenities: {', '.join([amenity for amenity in self.amenity])}\n"
        if self.tourism:
            description += f"Tourism: {', '.join([tourism for tourism in self.tourism])}\n"
        if self.historic:
            description += f"Historic: {', '.join([historic for historic in self.historic])}\n"
        if self.building:
            description += f"Building: {', '.join([building for building in self.building])}\n"
        if self.natural:
            description += f"Natural: {', '.join([natural for natural in self.natural])}\n"
        if self.water:
            description += f"Water: {', '.join([water for water in self.water])}\n"
        if self.leisure:
            description += f"Leisure: {', '.join([leisure for leisure in self.leisure])}\n"
        if self.man_made:
            description += f"Man-made: {', '.join([man_made for man_made in self.man_made])}\n"

        if description == "":
            return "No preferences set."
        
        return description

    def __set_amenity(self, amenity: dict) -> None | str:
        invalid_amenities = [a for a in amenity.keys() if a not in self.possible_amenity]
        if invalid_amenities:
            return f"Invalid amenity: {', '.join(invalid_amenities)}. Possible amenities are: {', '.join(self.possible_amenity)}"
        self.amenity = amenity

    def __set_tourism(self, tourism: dict) -> None | str:
        invalid_tourism = [t for t in tourism.keys() if t not in self.possible_tourism]
        if invalid_tourism:
            return f"Invalid tourism: {', '.join(invalid_tourism)}. Possible tourism are: {', '.join(self.possible_tourism)}"
        self.tourism = tourism

    def __set_historic(self, historic: dict) -> None | str:
        invalid_historic = [h for h in historic.keys() if h not in self.possible_historic]
        if invalid_historic:
            return f"Invalid historic: {', '.join(invalid_historic)}. Possible historic are: {', '.join(self.possible_historic)}"
        self.historic = historic

    def __set_building(self, building: dict) -> None | str:
        invalid_building = [b for b in building.keys() if b not in self.possible_building]
        if invalid_building:
            return f"Invalid building: {', '.join(invalid_building)}. Possible building are: {', '.join(self.possible_building)}"
        self.building = building

    def __set_natural(self, natural: dict) -> None | str:
        invalid_natural = [n for n in natural.keys() if n not in self.possible_natural]
        if invalid_natural:
            return f"Invalid natural: {', '.join(invalid_natural)}. Possible natural are: {', '.join(self.possible_natural)}"
        self.natural = natural

    def __set_water(self, water: dict) -> None | str:
        invalid_water = [w for w in water.keys() if w not in self.possible_water]
        if invalid_water:
            return f"Invalid water: {', '.join(invalid_water)}. Possible water are: {', '.join(self.possible_water)}"
        self.water = water

    def __set_leisure(self, leisure: dict) -> None | str:
        invalid_leisure = [l for l in leisure.keys() if l not in self.possible_leisure]
        if invalid_leisure:
            return f"Invalid leisure: {', '.join(invalid_leisure)}. Possible leisure are: {', '.join(self.possible_leisure)}"
        self.leisure = leisure

    def __set_man_made(self, man_made: dict) -> None | str:
        invalid_man_made = [m for m in man_made.keys() if m not in self.possible_man_made]
        if invalid_man_made:
            return f"Invalid man-made: {', '.join(invalid_man_made)}. Possible man-made are: {', '.join(self.possible_man_made)}"
        self.man_made = man_made

    def fill(self, amenity: None | dict = None, tourism: None | dict = None, historic: None | dict = None, building: None | dict = None, natural: None | dict = None, water: None | dict = None, leisure: None | dict = None, man_made: None | dict = None) -> None | str:
        """Fill the preferences descriptor with the given things
        Args:
            amenity (dict): A dictionary containing the amenity preferences to fill.
            tourism (dict): A dictionary containing the tourism preferences to fill.
            historic (dict): A dictionary containing the historic preferences to fill.
            building (dict): A dictionary containing the building preferences to fill.
            natural (dict): A dictionary containing the natural preferences to fill.
            water (dict): A dictionary containing the water preferences to fill.
            leisure (dict): A dictionary containing the leisure preferences to fill.
            man_made (dict): A dictionary containing the man-made preferences to fill.
        Raises:
            ValueError: If the key is not a valid attribute of the PreferencesDescriptor class
        
        Examples:
            ```python
            preferences = PreferencesDescriptor()
            preferences.fill(
                amenity={"restaurant": ["Italian", "Chinese"]},
                natural={"coastline": ["beach"]},
                historic={"castles": ["Neuschwanstein"]},
                building={"skyscrapers": ["Burj Khalifa"]},
                leisure={"parks": ["Central Park"]},
                man_made={"bridges": ["Golden Gate Bridge"]}
            )
            ```
        """
        if amenity is not None:
            res = self.__set_amenity(amenity)
            if res is not None:
                return res
        
        if tourism is not None:
            res = self.__set_tourism(tourism)
            if res is not None:
                return res

        if historic is not None:
            res = self.__set_historic(historic)
            if res is not None:
                return res

        if building is not None:
            res = self.__set_building(building)
            if res is not None:
                return res
            
        if natural is not None:
            res = self.__set_natural(natural)
            if res is not None:
                return res
            
        if water is not None:
            res = self.__set_water(water)
            if res is not None:
                return res
        
        if leisure is not None:
            res = self.__set_leisure(leisure)
            if res is not None:
                return res
            
        if man_made is not None:
            res = self.__set_man_made(man_made)
            if res is not None:
                return res

    def add_preference(self, cathegory: str, preference_type: str, preference_detail: list[str]) -> None | str:
        """Add a preference to the user preferences
        Args:
            - cathegory (str) : the category of the preference, e.g. "amenity", "tourism", etc.
            - preference_type (str) : the type of the preference, e.g. "restaurant", "museums", etc.
            - preference_detail (list[str]) : a list of details for the preference, e.g. ["Italian", "Chinese"]
        Examples:
            ```python
            add_preference(cathegory="amenity", preference_type="restaurant", preference_detail=["Italian", "Chinese"])
            ```
        """
        res = self.fill(
            **{cathegory: {preference_type: preference_detail}}
        )
        if res is not None:
            return res