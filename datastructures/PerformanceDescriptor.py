from pydantic import BaseModel


class PerformanceDescriptor(BaseModel):
    """Description of the user cycling performance"""
    kilometre_per_day: int = 0
    positive_height_difference_per_day: int = 0

    def get_kilometre_per_day(self) -> int:
        return self.kilometre_per_day
    
    def get_positive_height_difference_per_day(self) -> int:
        return self.positive_height_difference_per_day

    @classmethod
    def get_class_description(cls) -> str:
        """Get a string description of the class"""
        return f"""## PerformanceDescriptor:
- kilometre_per_day: int = 0
    - the maximum amount of kilometres the user is able to ride in a day
- positive_height_difference_per_day: int = 0
    - the maximum difference of height in meter the user is able to do in a day
"""

    def get_description(self) -> str:
        description = ""
        
        if self.kilometre_per_day > 0:
            description += f"kilometres per day: {self.kilometre_per_day}\n"
        if self.positive_height_difference_per_day > 0:
            description += f"Difference in height per day: {self.positive_height_difference_per_day}\n"
            
        if description == "":
            return "No performance set."

        return description
    
    def __set_kilometre_per_day(self, kilometre_per_day: int):
        if kilometre_per_day <= 0:
            raise Exception(f"Error in PerformanceDescriptor.__set_kilometre_per_day:\nkilometre_per_day must be greater than 0.\n{kilometre_per_day} was provided.")
        self.kilometre_per_day = kilometre_per_day

    def __set_positive_height_difference_per_day(self, positive_height_difference_per_day: int):
        if positive_height_difference_per_day < 0:
            raise Exception(f"Error in PerformanceDescriptor.__set_positive_height_difference_per_day:\npositive_height_difference_per_day must be at least 0.\n{positive_height_difference_per_day} was provided.")
        self.positive_height_difference_per_day = positive_height_difference_per_day

    def fill(self, kilometre_per_day: None | int = None, positive_height_difference_per_day: None | int = None):
        """Fill the performance descriptor with the given things
        Args:
            - kilometre_per_day (int | None) : the maximum amount of kilometres the user is able to ride in a day
            - positive_height_difference_per_day (int | None) : the maximum difference of height in meter the user is able to do in a day

        Returns:
            - None: if nothing went wrong
            - str: if something went wrong, it will return a string with the error message

        Examples:
            ```python
            performance = PerformanceDescriptor()
            performance.fill(kilometre_per_day=100, positive_height_difference_per_day=500)
            ```
        """
        if kilometre_per_day is not None:
            try:
                self.__set_kilometre_per_day(kilometre_per_day)
            except Exception as e:
                return e

        if positive_height_difference_per_day is not None:
            try:
                self.__set_positive_height_difference_per_day(positive_height_difference_per_day)
            except Exception as e:
                return e

        return None
