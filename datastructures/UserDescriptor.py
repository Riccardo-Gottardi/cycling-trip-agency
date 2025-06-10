from pydantic import BaseModel, Field


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometer_per_day: int = Field(default=0, description="the maximum amout of kilometers the user is able to ride in a day")
    difference_in_height_per_day: int = Field(default=0, description="the maximum difference of height in meter the user is ablo do in a day")

    def get_kilometer_per_day(self) -> int:
        return self.kilometer_per_day
    
    def get_difference_in_height_per_day(self) -> int:
        return self.difference_in_height_per_day
    
    def get_description(self) -> str:
        description = ""
        
        if self.kilometer_per_day > 0:
            description += f"Kilometers per day: {self.kilometer_per_day}\n"
        if self.difference_in_height_per_day > 0:
            description += f"Difference in height per day: {self.difference_in_height_per_day}\n"
            
        if description == "":
            return "No performance set."

        return description

    def fill(self, things: dict):
        for key in things.keys():
            if key == "kilometer_per_day":
                if not isinstance(things["kilometer_per_day"], int): raise TypeError(f"in PerformanceDescriptor.fill()\nThe given kilometer_per_day must be of type integer\n{type(things['kilometer_per_day'])} was provided")
                self.kilometer_per_day = things["kilometer_per_day"]

            elif key == "difference_in_height_per_day":
                if not isinstance(things["difference_in_height_per_day"], int): raise TypeError(f"in PerformanceDescriptor.fill()\nThe given difference_in_height_per_day must be of type integer\n{type(things['difference_in_height_per_day'])} was provided")
                self.difference_in_height_per_day = things["difference_in_height_per_day"]

            else:
                print(f"Warning: {key}, unexisting key was used when filling the performance descriptor")


class  PreferencesDescriptor(BaseModel):
    """Preference of the user for the points of interest"""
    amenity: list[str] | None = Field(default=None, description="Amenities that user prefers. Possible values: restaurant, cafe, bar, fast_food, pub, tourist_information, place_of_worship, parking, toilets, bench, drinking_water, bicycle_parking, bicycle_rental, bicycle_repair_station")
    turism: list[str] | None = Field(default=None, description="Tourism related points of interest. Possible values: museum, gallery, viewpoint, zoo, aquarium, theme_park, information, attraction")
    historic: list[str] | None = Field(default=None, description="Historic points of interest. Possible values: monument, memorial, castle, ruins, archaeological_site, fort, wayside_cross, wayside_shrine, battlefield, church, cathedral, mosque, synagogue, temple, tower")
    building: list[str] | None = Field(default=None, description="Buildings that are of interest. Possible values: cathedral, palace, castle, church, mosque, synagogue, temple")
    natural: list[str] | None = Field(default=None, description="Natural points of interest. Possible values: water, peak, volcano, coastline, beach, cave_entrance, waterfall, spring, glacier, wood, forest, wetland")
    water: list[str] | None = Field(default=None, description="Water related points of interest. Possible values: lake, river, pond, reservoir, canal")
    leisure: list[str] | None = Field(default=None, description="Leisure and recreational areas. Possible values: park, garden, nature_reserve, playground, resort, golf_course, stadium")
    man_made: list[str] | None = Field(default=None, description="Man-made structures that are of interest. Possible values: lighthouse, bridge, obelisk, tower")

    def get_description(self) -> str:
        description = ""

        if self.amenity:
            description += f"Amenities: {', '.join(self.amenity)}\n"
        if self.turism:
            description += f"Tourism: {', '.join(self.turism)}\n"
        if self.historic:
            description += f"Historic: {', '.join(self.historic)}\n"
        if self.building:
            description += f"Building: {', '.join(self.building)}\n"
        if self.natural:
            description += f"Natural: {', '.join(self.natural)}\n"
        if self.water:
            description += f"Water: {', '.join(self.water)}\n"
        if self.leisure:
            description += f"Leisure: {', '.join(self.leisure)}\n"
        if self.man_made:
            description += f"Man-made: {', '.join(self.man_made)}\n"

        if description == "":
            return "No preferences set."
        
        return description

    def fill(self, things: dict) -> None:
        """Fill the preferences descriptor with the given things
        Args:
            things (dict): A dictionary containing the preferences to fill. The keys must be one of the following:
                - amenity
                - turism
                - historic
                - building
                - natural
                - water
                - leisure
                - man_made
        Raises:
            ValueError: If the key is not a valid attribute of the PreferencesDescriptor class
        """
        for key in things.keys():
            if key == "amenity":
                if not isinstance(things["amenity"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given amenity must be of type list\n{type(things['amenity'])} was provided")
                self.amenity = things["amenity"]

            elif key == "turism":
                if not isinstance(things["turism"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given turism must be of type list\n{type(things['turism'])} was provided")
                self.turism = things["turism"]

            elif key == "historic":
                if not isinstance(things["historic"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given historic must be of type list\n{type(things['historic'])} was provided")
                self.historic = things["historic"]

            elif key == "building":
                if not isinstance(things["building"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given building must be of type list\n{type(things['building'])} was provided")
                self.building = things["building"]
                
            elif key == "natural":
                if not isinstance(things["natural"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given natural must be of type list\n{type(things['natural'])} was provided")
                self.natural = things["natural"]

            elif key == "water":
                if not isinstance(things["water"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given water must be of type list\n{type(things['water'])} was provided")
                self.water = things["water"]

            elif key == "leisure":
                if not isinstance(things["leisure"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given leisure must be of type list\n{type(things['leisure'])} was provided")
                self.leisure = things["leisure"]

            elif key == "man_made":
                if not isinstance(things["man_made"], list): raise TypeError(f"in PreferencesDescriptor.fill()\nThe given man_made must be of type list\n{type(things['man_made'])} was provided")
                self.man_made = things["man_made"]

            else:
                raise ValueError(f"in PreferencesDescriptor.fill()\nAttribute {key} is not a valid attribute of the PreferencesDescriptor class")

    def to_one_hot_encoding(self) -> set:
        """Convert the preferences to a one-hot encoding dictionary
        Examples:
            ```python
            preferences = PreferencesDescriptor(amenity=["restaurant", "cafe"], turism=["museum"])
            one_hot = preferences.to_one_hot_encoding()
            ```
        """
        one_hot = set()

        if self.amenity is not None:
            one_hot.update(self.amenity)
        if self.turism is not None:
            one_hot.update(self.turism)
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
        user.fill({
            "performance": {
                "kilometer_per_day": 100,
                "difference_in_height_per_day": 500
            },
        })
        performance = user.get_performance()
        ```
    """
    performance: PerformanceDescriptor = Field(default=PerformanceDescriptor(), description="measure of the user cycling performance of the user")
    preferences: PreferencesDescriptor = Field(default=PreferencesDescriptor(), description="preferences of the user for the points of interest")

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

    def get_description(self) -> str:
        """Get a string description of the user"""
        return f"User performance: {self.performance.get_description()}, User preferences: {self.preferences.get_description()}"

    def fill(self, things: dict) -> None:
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
            user.fill({
                "performance": {
                    "kilometer_per_day": 100,
                    "difference_in_height_per_day": 500
                },
                "preferences": {
                    "amenity": ["restaurant", "cafe"],
                    "turism": ["museum"]
                }
            })
            ```
        """
        for key in things.keys():
            if key == "performance":
                self.performance.fill(things["performance"])

            elif key == "preferences":
                self.preferences.fill(things["preferences"])

            else:
                raise ValueError(f"in UserDescription.fill()\nAttribute {key} cannot be filled by the user, or it is not a valid attribute of the UserDescription class")
            
