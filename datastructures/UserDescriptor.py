from pydantic import BaseModel
from datastructures.PerformanceDescriptor import PerformanceDescriptor
from datastructures.PreferencesDescriptor import PreferencesDescriptor

class UserDescriptor(BaseModel):
    """Description of the user
    Attributes:
        performance (PerformanceDescriptor): measure of the user cycling performance of the user
        preferences (PreferencesDescriptor): preferences of the user for the points of interest
        additional_note: a useful additional note about the user, that might fell off from performance and preferences

    Examples:
        ```python
        user = UserDescriptor()
        user.fill(
            performance = {
                "kilometer_per_day": 100,
                "positive_height_difference_per_day": 500
            }
        )
        performance = user.get_performance()
        ```
    """
    performance: PerformanceDescriptor = PerformanceDescriptor() 
    preferences: PreferencesDescriptor = PreferencesDescriptor()
    additional_note: str = ""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # This is where you would typically load the user from a persistence system
        # Check if the user exist in the persistance system
        #   If yes, load his performance and preferences
        #   If no, do nothing

    def get_performance(self) -> PerformanceDescriptor:
        """Get the performance descriptor of the user"""
        return self.performance
    
    def get_preferences(self) -> PreferencesDescriptor:
        """Get the preferences descriptor of the user"""
        return self.preferences

    def get_additional_note(self) -> str:
        """Get the additional notes about the user"""
        return self.additional_note

    def get_class_description(self) -> str:
        """Get a string description of the class that represent the user"""
        return f"""# UserDescriptor:
- performance: PerformanceDescriptor
- preferences: PreferenceDescriptor
- addional_note: str
{self.performance.get_class_description()}
{self.preferences.get_class_description()}
## Additional note
{self.additional_note}
"""

    def get_description(self) -> str:
        """Get a string description of the user"""
        return f"User performance: {self.performance.get_description()}, User preferences: {self.preferences.get_description()}, Additional note: {self.additional_note}"

    def __set_performance(self, performance : dict) -> None | str:
        kilometer_per_day = performance.get("kilometer_per_day", None)
        positive_height_difference_per_day = performance.get("positive_height_difference_per_day", None)
        res = self.performance.fill(
            kilometer_per_day=kilometer_per_day,
            positive_height_difference_per_day=positive_height_difference_per_day
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
        
    def __set_additional_notes(self, additional_note: str) -> None | str:
        self.additional_note = additional_note

    def fill(self, performance: None | dict = None, preferences: None | dict = None, additional_note: None | str = None) -> None | str:
        """Fill the user descriptor with the given things
        Args:
            - performance (dict | None) : a dictionary containing the performance to fill. The keys must be one of the following:
                - kilometer_per_day
                - positive_height_difference_per_day
            - preferences (dict | None) : a dictionary containing the preferences to fill. The keys must be one of the following:
                - amenity
                - tourism
                - historic
                - building
                - natural
                - water
                - leisure
                - man_made
            - additional_note (str | None) : additional notes about the user (that might fall outside the performance and preferences)
        Raises:
            ValueError: If the key is not a valid attribute of the UserDescriptor class
        Examples:
            ```python
            user = UserDescriptor()
            user.fill(
                performance = {
                    "kilometer_per_day": 100,
                    "positive_height_difference_per_day": 500
                },
                preferences = {
                    "amenity": ["restaurant", "cafe"],
                    "tourism": ["museum"]
                }
            )
            ...
            user.fill(additional_note = "The user like to go throug tough climbs"
            ```
        """
        if performance != None:
            res = self.__set_performance(performance)
            if res != None:
                return res
            
        if preferences != None:
            res = self.__set_preferences(preferences)
            if res != None:
                return res
        
        if additional_note: # that way it covers both None and "", without using an and statement
            res = self.__set_additional_notes(additional_note)
            if res != None:
                return res
