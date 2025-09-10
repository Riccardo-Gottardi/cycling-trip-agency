from pydantic import BaseModel


class  POIsDescriptor(BaseModel):
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
        return f"""## POIsDescriptor:
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

        if self.amenity is not None:
            description += f"Amenities: {', '.join([amenity for amenity in self.amenity])}\n"
        if self.tourism is not None:
            description += f"Tourism: {', '.join([tourism for tourism in self.tourism])}\n"
        if self.historic is not None:
            description += f"Historic: {', '.join([historic for historic in self.historic])}\n"
        if self.building is not None:
            description += f"Building: {', '.join([building for building in self.building])}\n"
        if self.natural is not None:
            description += f"Natural: {', '.join([natural for natural in self.natural])}\n"
        if self.water is not None:
            description += f"Water: {', '.join([water for water in self.water])}\n"
        if self.leisure is not None:
            description += f"Leisure: {', '.join([leisure for leisure in self.leisure])}\n"
        if self.man_made is not None:
            description += f"Man-made: {', '.join([man_made for man_made in self.man_made])}\n"

        if description == "":
            return "No preferences set."
        
        return description

    def __set_amenity(self, p_type: str, detail: list[str]):
        if p_type not in self.possible_amenity:
            raise Exception(f"Invalid amenity type: {p_type}. Possible p_types are: {', '.join(self.possible_amenity)}")
        self.amenity = {p_type: detail}

    def __set_tourism(self, p_type : str, detail: list[str]):
        if{p_type}not in self.possible_tourism:
            raise Exception(f"Invalid tourism type: {p_type}. Possible p_types are: {', '.join(self.possible_tourism)}")
        self.tourism = {p_type: detail}

    def __set_historic(self, p_type : str, detail: list[str]):
        if{p_type}not in self.possible_historic:
            raise Exception(f"Invalid historic type: {p_type}. Possible p_types are: {', '.join(self.possible_historic)}")
        self.historic = {p_type: detail}

    def __set_building(self, p_type : str, detail: list[str]):
        if{p_type}not in self.possible_building:
            raise Exception(f"Invalid building type: {p_type}. Possible p_types are: {', '.join(self.possible_building)}")
        self.building = {p_type: detail}

    def __set_natural(self, p_type : str, detail: list[str]):
        if{p_type}not in self.possible_natural:
            raise Exception(f"Invalid natural type: {p_type}. Possible p_types are: {', '.join(self.possible_natural)}")
        self.natural = {p_type: detail}

    def __set_water(self, p_type : str, detail: list[str]):
        if{p_type}not in self.possible_water:
            raise Exception(f"Invalid water type: {p_type}. Possible p_types are: {', '.join(self.possible_water)}")
        self.water = {p_type: detail}

    def __set_leisure(self, p_type : str, detail: list[str]) -> None | str:
        if{p_type}not in self.possible_leisure:
            raise Exception(f"Invalid leisure type: {p_type}. Possible p_types are: {', '.join(self.possible_leisure)}")
        self.leisure = {p_type: detail}

    def __set_man_made(self, p_type : str, detail: list[str]) -> None | str:
        if{p_type}not in self.possible_man_made:
            raise Exception(f"Invalid man-made type: {p_type}. Possible p_types are: {', '.join(self.possible_man_made)}")
        self.man_made = {p_type: detail}

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
            ValueError: If the key is not a valid attribute of the POIsDescriptor class
        
        Examples:
            ```python
            preferences = POIsDescriptor()
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
            try:
                for p_type, detail in amenity.items():
                    self.__set_amenity(p_type, detail)
            except Exception as e:
                raise e

        if tourism is not None:
            try:
                for p_type, detail in tourism.items():
                    self.__set_tourism(p_type, detail)
            except Exception as e:
                raise e

        if historic is not None:
            try:
                for p_type, detail in historic.items():
                    self.__set_historic(p_type, detail)
            except Exception as e:
                raise e

        if building is not None:
            try:
                for p_type, detail in building.items():
                    self.__set_building(p_type, detail)
            except Exception as e:
                raise e

        if natural is not None:
            try:
                for p_type, detail in natural.items():
                    self.__set_natural(p_type, detail)
            except Exception as e:
                raise e

        if water is not None:
            try:
                for p_type, detail in water.items():
                    self.__set_water(p_type, detail)
            except Exception as e:
                raise e

        if leisure is not None:
            try:
                for p_type, detail in leisure.items():
                    self.__set_leisure(p_type, detail)
            except Exception as e:
                raise e

        if man_made is not None:
            try:
                for p_type, detail in man_made.items():
                    self.__set_man_made(p_type, detail)
            except Exception as e:
                raise e

    def add_preference(self, category: str, preference_type: str, preference_detail: list[str]) -> None | str:
        """Add a preference to the user preferences
        Args:
            - category (str) : the category of the preference, e.g. "amenity", "tourism", etc.
            - preference_type (str) : the type of the preference, e.g. "restaurant", "museums", etc.
            - preference_detail (list[str]) : a list of details for the preference, e.g. ["Italian", "Chinese"]
        Examples:
            ```python
            add_preference(category="amenity", preference_type="restaurant", preference_detail=["Italian", "Chinese"])
            ```
        """
        try:
            match category:
                case "amenity":
                    self.__set_amenity(preference_type, preference_detail)
                case "tourism":
                    self.__set_tourism(preference_type, preference_detail)
                case "historic":
                    self.__set_historic(preference_type, preference_detail)
                case "building":
                    self.__set_building(preference_type, preference_detail)
                case "natural":
                    self.__set_natural(preference_type, preference_detail)
                case "water":
                    self.__set_water(preference_type, preference_detail)
                case "leisure":
                    self.__set_leisure(preference_type, preference_detail)
                case "man_made":
                    self.__set_man_made(preference_type, preference_detail)
        except Exception as e:
            raise e