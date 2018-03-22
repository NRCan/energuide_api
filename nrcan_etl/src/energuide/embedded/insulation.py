class Insulation:
    _RSI_MULTIPLIER = 5.678263337

    def __init__(self, rsi: float) -> None:
        self._rsi = rsi

    @property
    def rsi(self) -> float:
        return self._rsi

    @property
    def r_value(self) -> float:
        return self._rsi * self._RSI_MULTIPLIER

    @classmethod
    def from_r_value(cls, r_value: float) -> 'Insulation':
        return cls(r_value / cls._RSI_MULTIPLIER)

    def __eq__(self, other):
        return isinstance(other, Insulation) and self._rsi == other._rsi

    def __repr__(self):
        return f'Insulation(rsi={self._rsi})'
