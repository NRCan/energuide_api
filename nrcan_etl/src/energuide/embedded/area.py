class Area:
    _FEET_SQUARED_MULTIPLIER = 3.28084 ** 2

    def __init__(self, area_metric: float) -> None:
        self._area_metric = float(area_metric)

    @property
    def square_metres(self) -> float:
        return self._area_metric

    @property
    def square_feet(self) -> float:
        return self._area_metric * self._FEET_SQUARED_MULTIPLIER

    @classmethod
    def from_square_feet(cls, area_square_feet: float) -> 'Area':
        return cls(area_square_feet / cls._FEET_SQUARED_MULTIPLIER)

    def __eq__(self, other):
        return isinstance(other, Area) and self._area_metric == other._area_metric

    def __repr__(self):
        return f'Area(area_metric={self._area_metric})'
