from pydantic import BaseModel, Field


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometer_per_day: int = Field(default=0, description="the maximum amout of kilometers the user is able to ride in a day")
    difference_in_height_per_day: int = Field(default=0, description="the maximum difference of height in meter the user is ablo do in a day")

    def get_kilometer_per_day(self) -> int:
        return self.kilometer_per_day
    
    def get_difference_in_height_per_day(self) -> int:
        return self.difference_in_height_per_day

    def fill(self, things: dict):
        for key in things.keys():
            if key == "kilometer_per_day":
                assert isinstance(things["kilometer_per_day"], int), f"in PerformanceDescriptor.fill()\nThe given kilometer_per_day must be of type integer\n{things['kilometer_per_day'].__class__} was provided"
                self.kilometer_per_day = things["kilometer_per_day"]

            elif key == "difference_in_height_per_day":
                assert isinstance(things["difference_in_height_per_day"], int), f"in PerformanceDescriptor.fill()\nThe given difference_in_height_per_day must be of type integer\n{things['difference_in_height_per_day'].__class__} was provided"
                self.difference_in_height_per_day = things["difference_in_height_per_day"]

            else:
                print(f"Warning: {key}, unexisting key was used when filling the performance descriptor")

    def debug_dict(self) -> dict:
        return {
            "kilometer_per_day": {"class": self.get_kilometer_per_day().__class__, "value": self.get_kilometer_per_day()},
            "difference_in_height_per_day": {"class": self.get_difference_in_height_per_day().__class__, "value": self.get_difference_in_height_per_day()}
        }


class  PreferencesDescriptor(BaseModel):
    """Preference of the user for the points of interest"""
    amenity: list[str] | None = Field(default=None, description="Amenities that user prefers. Possible values: restaurant, cafe, bar, fast_food, pub, tourist_information, place_of_worship, parking, toilets, bench, drinking_water, bicycle_parking, bicycle_rental, bicycle_repair_station")
    turism: list[str] | None = Field(default=None, description="Tourism related points of interest. Possible values: museum, gallery, viewpoint, zoo, aquarium, theme_park, information, attraction")
    historic: list[str] | None = Field(default=None, description="Historic points of interest. Possible values: monument, memorial, castle, ruins, archaeological_site, fort, wayside_cross, wayside_shrine, battlefield, church, cathedral, mosque, synagogue, temple, tower")
    building: list[str] | None = Field(default=None, description="Buildings that are of interest. Possible values: cathedral, palace, castle, church, mosque, synagogue, temple")
    natural: list[str] | None = Field(default=None, description="Natural points of interest. Possible values: water, peak, volcano, coastline, beach, cave_entrance, waterfall, spring, glacier, wood, forest, wetland")
    water: list[str] | None = Field(default=None, description="Water related points of interest. Possible values: lake, river, pond, reservoir, canal")
    laisure: list[str] | None = Field(default=None, description="Leisure and recreational areas. Possible values: park, garden, nature_reserve, playground, resort, golf_course, stadium")
    man_made: list[str] | None = Field(default=None, description="Man-made structures that are of interest. Possible values: lighthouse, bridge, obelisk, tower")

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
                - laisure
                - man_made
        Raises:
            ValueError: If the key is not a valid attribute of the PreferencesDescriptor class
        """
        for key in things.keys():
            if key == "amenity":
                assert isinstance(things["amenity"], list), f"in PreferencesDescriptor.fill()\nThe given amenity must be of type list\n{things['amenity'].__class__} was provided"
                self.amenity = things["amenity"]

            elif key == "turism":
                assert isinstance(things["turism"], list), f"in PreferencesDescriptor.fill()\nThe given turism must be of type list\n{things['turism'].__class__} was provided"
                self.turism = things["turism"]

            elif key == "historic":
                assert isinstance(things["historic"], list), f"in PreferencesDescriptor.fill()\nThe given historic must be of type list\n{things['historic'].__class__} was provided"
                self.historic = things["historic"]

            elif key == "building":
                assert isinstance(things["building"], list), f"in PreferencesDescriptor.fill()\nThe given building must be of type list\n{things['building'].__class__} was provided"
                self.building = things["building"]
                
            elif key == "natural":
                assert isinstance(things["natural"], list), f"in PreferencesDescriptor.fill()\nThe given natural must be of type list\n{things['natural'].__class__} was provided"
                self.natural = things["natural"]

            elif key == "water":
                assert isinstance(things["water"], list), f"in PreferencesDescriptor.fill()\nThe given water must be of type list\n{things['water'].__class__} was provided"
                self.water = things["water"]

            elif key == "laisure":
                assert isinstance(things["laisure"], list), f"in PreferencesDescriptor.fill()\nThe given laisure must be of type list\n{things['laisure'].__class__} was provided"
                self.laisure = things["laisure"]

            elif key == "man_made":
                assert isinstance(things["man_made"], list), f"in PreferencesDescriptor.fill()\nThe given man_made must be of type list\n{things['man_made'].__class__} was provided"
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
        if self.laisure is not None:
            one_hot.update(self.laisure)
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
        """
        for key in things.keys():
            if key == "performance":
                assert isinstance(things["performance"], dict), f"in UserDescription.fill()\nThe given performance must be of type dict\n{things['performance'].__class__} was provided"
                self.performance.fill(things["performance"])

            elif key == "preferences":
                assert isinstance(things["preferences"], dict), f"in UserDescription.fill()\nThe given preferences must be of type dict\n{things['preferences'].__class__} was provided"
                self.preferences.fill(things["preferences"])

            else:
                raise ValueError(f"in UserDescription.fill()\nAttribute {key} cannot be filled by the user, or it is not a valid attribute of the UserDescription class")
