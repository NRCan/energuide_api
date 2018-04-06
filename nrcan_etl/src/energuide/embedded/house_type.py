import re


class HouseType():
    
    @classmethod
    def normalize(cls, unclean_string) -> str:
        lowercase = unclean_string.lower()
        alpha = re.sub('[^a-zA-Z/ _-]', '', lowercase)
        separated = re.sub('[_-]', ' ', alpha)

        return separated.capitalize()
