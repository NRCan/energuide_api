class Distance:
    _FEET_MULTIPLIER = 3.28084

    def __init__(self, distance_metres: float) -> None:
        self._distance = distance_metres

    @property
    def metres(self) -> float:
        return self._distance

    @property
    def feet(self) -> float:
        return self._distance * self._FEET_MULTIPLIER

    @classmethod
    def from_feet(cls, distance_feet) -> 'Distance':
        return cls(distance_feet / cls._FEET_MULTIPLIER)

    def __eq__(self, other):
        return isinstance(other, Distance) and self._distance == other._distance

    def __repr__(self):
        return f'Distance(distance_metres={self._distance})'
