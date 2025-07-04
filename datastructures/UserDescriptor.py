from pydantic import BaseModel


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometer_per_day: int = 0 #Field(default=0, description="the maximum amout of kilometers the user is able to ride in a day")
    difference_in_height_per_day: int = 0 #Field(default=0, description="the maximum difference of height in meter the user is ablo do in a day")

    def get_kilometer_per_day(self) -> int:
        return self.kilometer_per_day
    
    def get_difference_in_height_per_day(self) -> int:
        return self.difference_in_height_per_day

    def get_class_description(self) -> str:
        """Get a string description of the class"""
        return f"""PerformanceDescriptor:
    - kilometer_per_day: int = 0
        - the maximum amount of kilometers the user is able to ride in a day
    - difference_in_height_per_day: int = 0
        - the maximum difference of height in meter the user is able to do in a day
"""

    def get_description(self) -> str:
        description = ""
        
        if self.kilometer_per_day > 0:
            description += f"Kilometers per day: {self.kilometer_per_day}\n"
        if self.difference_in_height_per_day > 0:
            description += f"Difference in height per day: {self.difference_in_height_per_day}\n"
            
        if description == "":
            return "No performance set."

        return description
    
    def __set_kilometer_per_day(self, kilometer_per_day: int) -> None | str:
        self.kilometer_per_day = kilometer_per_day

    def __set_difference_in_height_per_day(self, difference_in_height_per_day: int) -> None | str:
        self.difference_in_height_per_day = difference_in_height_per_day

    def fill(self, kilometer_per_day: None | int = None, difference_in_height_per_day: None | int = None) -> None | str:
        if kilometer_per_day != None:
            res = self.__set_kilometer_per_day(kilometer_per_day)
            if res != None:
                return res
        
        if difference_in_height_per_day != None:
            res = self.__set_difference_in_height_per_day(difference_in_height_per_day)
            if res != None:
                return res


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
    amenity: list[str] | None = None
    tourism: list[str] | None = None
    historic: list[str] | None = None
    building: list[str] | None = None
    natural: list[str] | None = None
    water: list[str] | None = None
    leisure: list[str] | None = None
    man_made: list[str] | None = None

    def get_amenity(self) -> list[str] | None:
        return self.amenity
    
    def get_tourism(self) -> list[str] | None:
        return self.tourism
    
    def get_historic(self) -> list[str] | None:
        return self.historic
    
    def get_building(self) -> list[str] | None:
        return self.building
    
    def get_natural(self) -> list[str] | None:
        return self.natural
    
    def get_water(self) -> list[str] | None:
        return self.water
    
    def get_leisure(self) -> list[str] | None:
        return self.leisure
    
    def get_man_made(self) -> list[str] | None:
        return self.man_made
    
    def get_class_description(self) -> str:
        """Get a string description of the class"""
        return f"""PreferencesDescriptor:
    - amenity: list[str] | None = None
        - the list of amenities the user prefers
        - can be one or more of the following: {', '.join(self.possible_amenity)}
    - tourism: list[str] | None = None
        - the list of tourism points the user prefers
        - can be one or more of the following: {', '.join(self.possible_tourism)}
    - historic: list[str] | None = None
        - the list of historic points the user prefers
        - can be one or more of the following: {', '.join(self.possible_historic)}
    - building: list[str] | None = None
        - the list of buildings the user prefers
        - can be one or more of the following: {', '.join(self.possible_building)}
    - natural: list[str] | None = None
        - the list of natural points the user prefers
        - can be one or more of the following: {', '.join(self.possible_natural)}
    - water: list[str] | None = None
        - the list of water points the user prefers
        - can be one or more of the following: {', '.join(self.possible_water)}
    - leisure: list[str] | None = None
        - the list of leisure points the user prefers
        - can be one or more of the following: {', '.join(self.possible_leisure)}
    - man_made: list[str] | None = None
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

    def __set_amenity(self, amenity: list[str]) -> None | str:
        invalid_amenities = [a for a in amenity if a not in self.possible_amenity]
        if invalid_amenities:
            return f"Invalid amenity: {', '.join(invalid_amenities)}. Possible amenities are: {', '.join(self.possible_amenity)}"
        self.amenity = amenity

    def __set_tourism(self, tourism: list[str]) -> None | str:
        invalid_tourism = [t for t in tourism if t not in self.possible_tourism]
        if invalid_tourism:
            return f"Invalid tourism: {', '.join(invalid_tourism)}. Possible tourism are: {', '.join(self.possible_tourism)}"
        self.tourism = tourism

    def __set_historic(self, historic: list[str]) -> None | str:
        invalid_historic = [h for h in historic if h not in self.possible_historic]
        if invalid_historic:
            return f"Invalid historic: {', '.join(invalid_historic)}. Possible historic are: {', '.join(self.possible_historic)}"
        self.historic = historic

    def __set_building(self, building: list[str]) -> None | str:
        invalid_building = [b for b in building if b not in self.possible_building]
        if invalid_building:
            return f"Invalid building: {', '.join(invalid_building)}. Possible building are: {', '.join(self.possible_building)}"
        self.building = building

    def __set_natural(self, natural: list[str]) -> None | str:
        invalid_natural = [n for n in natural if n not in self.possible_natural]
        if invalid_natural:
            return f"Invalid natural: {', '.join(invalid_natural)}. Possible natural are: {', '.join(self.possible_natural)}"
        self.natural = natural

    def __set_water(self, water: list[str]) -> None | str:
        invalid_water = [w for w in water if w not in self.possible_water]
        if invalid_water:
            return f"Invalid water: {', '.join(invalid_water)}. Possible water are: {', '.join(self.possible_water)}"
        self.water = water

    def __set_leisure(self, leisure: list[str]) -> None | str:
        invalid_leisure = [l for l in leisure if l not in self.possible_leisure]
        if invalid_leisure:
            return f"Invalid leisure: {', '.join(invalid_leisure)}. Possible leisure are: {', '.join(self.possible_leisure)}"
        self.leisure = leisure

    def __set_man_made(self, man_made: list[str]) -> None | str:
        invalid_man_made = [m for m in man_made if m not in self.possible_man_made]
        if invalid_man_made:
            return f"Invalid man-made: {', '.join(invalid_man_made)}. Possible man-made are: {', '.join(self.possible_man_made)}"
        self.man_made = man_made

    def fill(self, amenity: None | list[str] = None, tourism: None | list[str] = None, historic: None | list[str] = None, building: None | list[str] = None, natural: None | list[str] = None, water: None | list[str] = None, leisure: None | list[str] = None, man_made: None | list[str] = None) -> None | str:
        """Fill the preferences descriptor with the given things
        Args:
            things: A dictionary containing the preferences to fill. The keys must be one of the following:
                - amenity
                - tourism
                - historic
                - building
                - natural
                - water
                - leisure
                - man_made

        Raises:
            ValueError: If the key is not a valid attribute of the PreferencesDescriptor class
        
        Examples:
            ```python
            preferences = PreferencesDescriptor()
            preferences.fill(
                amenity=["restaurant", "cafe"],
                tourism=["museum"],
            )
            ```
        """
        if amenity != None:
            res = self.__set_amenity(amenity=amenity)
            if res != None:
                return res
        
        if tourism != None:
            res = self.__set_tourism(tourism=tourism)
            if res != None:
                return res

        if historic != None:
            res = self.__set_historic(historic=historic)
            if res != None:
                return res

        if building != None:
            res = self.__set_building(building=building)
            if res != None:
                return res
            
        if natural != None:
            res = self.__set_natural(natural=natural)
            if res != None:
                return res
            
        if water != None:
            res = self.__set_water(water=water)
            if res != None:
                return res
        
        if leisure != None:
            res = self.__set_leisure(leisure=leisure)
            if res != None:
                return res
            
        if man_made != None:
            res = self.__set_man_made(man_made=man_made)
            if res != None:
                return res

    def to_one_hot_encoding(self) -> set:
        """Convert the preferences to a one-hot encoding dictionary
        Examples:
            ```python
            preferences = PreferencesDescriptor(amenity=["restaurant", "cafe"], tourism=["museum"])
            one_hot = preferences.to_one_hot_encoding()
            ```
        """
        one_hot = set()

        if self.amenity is not None:
            one_hot.update(self.amenity)
        if self.tourism is not None:
            one_hot.update(self.tourism)
        if self.historic is not None:
            one_hot.update(self.historic)
        if self.building is not None:
            one_hot.update(self.building)
        if self.natural is not None:
            one_hot.update(self.natural)
        if self.water is not None:
            one_hot.update(self.water)
        if self.leisure is not None:
            one_hot.update(self.leisure)
        if self.man_made is not None:
            one_hot.update(self.man_made)

        return one_hot


class UserDescriptor(BaseModel):
    """Description of the user
    Attributes:
        performance (PerformanceDescriptor): measure of the user cycling performance of the user
        preferences (PreferencesDescriptor): preferences of the user for the points of interest

    Examples:
        ```python
        user = UserDescriptor()
        user.fill(
            performance = {
                "kilometer_per_day": 100,
                "difference_in_height_per_day": 500
            }
        )
        performance = user.get_performance()
        ```
    """
    performance: PerformanceDescriptor = PerformanceDescriptor() 
    preferences: PreferencesDescriptor = PreferencesDescriptor() 

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Check if the user exist in the persistance system
        # If yes, load his performance and preferences
        # If no, do nothing

    def get_performance(self) -> PerformanceDescriptor:
        """Get the performance descriptor of the user"""
        return self.performance
    
    def get_preferences(self) -> PreferencesDescriptor:
        """Get the preferences descriptor of the user"""
        return self.preferences

    def get_class_description(self) -> str:
        """Get a string description of the class that represent the user"""
        return f"""UserDescriptor:
    - performance: PerformanceDescriptor = {self.performance.get_class_description()}
    - preferences: PreferencesDescriptor = {self.preferences.get_class_description()}
"""

    def get_description(self) -> str:
        """Get a string description of the user"""
        return f"User performance: {self.performance.get_description()}, User preferences: {self.preferences.get_description()}"

    def __set_performance(self, performance : dict) -> None | str:
        kilometer_per_day = performance.get("kilometer_per_day", None)
        difference_in_height_per_day = performance.get("difference_in_height_per_day", None)
        res = self.performance.fill(
            kilometer_per_day=kilometer_per_day,
            difference_in_height_per_day=difference_in_height_per_day
        )
        if res != None: 
            return res

    def __set_preferences(self, preferences : dict) -> None | str:
        amenity = preferences.get("amenity", None)
        tourism = preferences.get("tourism", None)
        historic = preferences.get("historic", None)
        building = preferences.get("building", None)
        natural = preferences.get("natural", None)
        water = preferences.get("water", None)
        leisure = preferences.get("leisure", None)
        man_made = preferences.get("man_made", None)
        res = self.preferences.fill(
            amenity=amenity,
            tourism=tourism,
            historic=historic,
            building=building,
            natural=natural,
            water=water,
            leisure=leisure,
            man_made=man_made
        )
        if res != None:
            return res

    def fill(self, performance: None | dict = None, preferences: None | dict = None) -> None | str:
        """Fill the user descriptor with the given things
        Args:
            things (dict): A dictionary containing the user description to fill. The keys must be one of the following:
                - performance
                - preferences
        Raises:
            ValueError: If the key is not a valid attribute of the UserDescriptor class
        Examples:
            ```python
            user = UserDescriptor()
            user.fill(
                performance = {
                    "kilometer_per_day": 100,
                    "difference_in_height_per_day": 500
                },
                preferences = {
                    "amenity": ["restaurant", "cafe"],
                    "tourism": ["museum"]
                }
            )
            ```
        """
        if performance != None:
            res = self.__set_performance(performance=performance)
            if res != None:
                return res
            
        if preferences != None:
            res = self.__set_preferences(preferences=preferences)
            if res != None:
                return res
            
