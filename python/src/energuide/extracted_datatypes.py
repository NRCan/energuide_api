import typing

class _Ceiling(typing.NamedTuple):
    label: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    nominal_rsi: typing.Optional[float]
    effective_rsi: typing.Optional[float]
    area_metres: typing.Optional[float]
    length_metres: typing.Optional[float]


class _Floor(typing.NamedTuple):
    label: typing.Optional[str]
    nominal_rsi: typing.Optional[float]
    effective_rsi: typing.Optional[float]
    area_metres: typing.Optional[float]
    length_metres: typing.Optional[float]


class _Wall(typing.NamedTuple):
    label: typing.Optional[str]
    structure_type_english: typing.Optional[str]
    structure_type_french: typing.Optional[str]
    component_type_size_english: typing.Optional[str]
    component_type_size_french: typing.Optional[str]
    nominal_rsi: typing.Optional[float]
    effective_rsi: typing.Optional[float]
    perimeter: typing.Optional[float]
    height: typing.Optional[float]

_RSI_MULTIPLIER = 5.678263337
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2


class Wall(_Wall):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'label':  {'type': 'string', 'required': True},
                'constructionTypeCode':  {'type': 'string', 'required': False},
                'constructionTypeNode':  {'type': 'string', 'required': False},
                'nominalRsi':  {'type': 'float', 'required': True, 'coerce': float},
                'effectiveRsi':  {'type': 'float', 'required': True, 'coerce': float},
                'perimeter':  {'type': 'float', 'required': True, 'coerce': float},
                'height':  {'type': 'float', 'required': True, 'coerce': float},
            }
        }
    }

    @classmethod
    def from_data(cls,
                  wall: typing.Dict[str, typing.Any],
                  wall_codes: typing.Dict[str, typing.Dict[str, typing.Optional[str]]]):

        code_id = wall.get('constructionTypeCode')
        code = wall_codes.get(code_id) if code_id is not None else None

        structure_type_english = code['structureTypeEnglish'] if code is not None else None
        structure_type_french = code['structureTypeFrench'] if code is not None else None
        component_type_size_english = code['componentTypeSizeEnglish'] if code is not None else None
        component_type_size_french = code['componentTypeSizeFrench'] if code is not None else None

        return Wall(
            label=wall['label'],
            structure_type_english=structure_type_english,
            structure_type_french=structure_type_french,
            component_type_size_english=component_type_size_english,
            component_type_size_french=component_type_size_french,
            nominal_rsi=wall['nominalRsi'],
            effective_rsi=wall['effectiveRsi'],
            perimeter=wall['perimeter'],
            height=wall['height'],
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'structureTypeEnglish': self.structure_type_english,
            'structureTypeFrench': self.structure_type_french,
            'componentTypeSizeEnglish': self.component_type_size_english,
            'componentTypeSizeFrench': self.component_type_size_french,
            'nominalRsi': self.nominal_rsi,
            'nominalR': (self.nominal_rsi * _RSI_MULTIPLIER) if self.nominal_rsi is not None else None,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': (self.effective_rsi * _RSI_MULTIPLIER) if self.effective_rsi is not None else None,
            'areaMetres': self.perimeter * self.height,
            'areaFeet': (self.perimeter * self.height * _FEET_SQUARED_MULTIPLIER)
                         if (self.perimeter is not None and self.height is not None) else None,
            'perimeter': self.perimeter,
            'height': self.height,
        }

class Ceiling(_Ceiling):
    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'label': {'type': 'string', 'required': True},
                'typeEnglish': {'type': 'string', 'required': True},
                'typeFrench': {'type': 'string', 'required': True},
                'nominalRsi': {'type': 'float', 'required': True, 'coerce': float},
                'effectiveRsi': {'type': 'float', 'required': True, 'coerce': float},
                'area': {'type': 'float', 'required': True, 'coerce': float},
                'length': {'type': 'float', 'required': True, 'coerce': float}
            }
        }
    }

    @classmethod
    def from_data(cls, ceiling: typing.Dict[str, typing.Any]):
        return Ceiling(
            label=ceiling['label'],
            type_english=ceiling['typeEnglish'],
            type_french=ceiling['typeFrench'],
            nominal_rsi=ceiling['nominalRsi'],
            effective_rsi=ceiling['effectiveRsi'],
            area_metres=ceiling['area'],
            length_metres=ceiling['length']

        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'typeEnglish': self.type_english,
            'typeFrench': self.type_french,
            'nominalRsi': self.nominal_rsi,
            'nominalR': (self.nominal_rsi * _RSI_MULTIPLIER) if self.nominal_rsi is not None else None,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': (self.effective_rsi * _RSI_MULTIPLIER) if self.effective_rsi is not None else None,
            'areaMetres': self.area_metres,
            'areaFeet': (self.area_metres * _FEET_SQUARED_MULTIPLIER) if self.area_metres is not None else None,
            'lengthMetres': self.length_metres,
            'lengthFeet': (self.length_metres * _FEET_MULTIPLIER) if self.length_metres is not None else None
        }


class Floor(_Floor):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'label': {'type': 'string', 'required': True},
                'nominalRsi': {'type': 'float', 'required': True, 'coerce': float},
                'effectiveRsi': {'type': 'float', 'required': True, 'coerce': float},
                'area': {'type': 'float', 'required': True, 'coerce': float},
                'length': {'type': 'float', 'required': True, 'coerce': float}
            }
        }
    }

    @classmethod
    def from_data(cls, ceiling: typing.Dict[str, typing.Any]):
        return Floor(
            label=ceiling['label'],
            nominal_rsi=ceiling['nominalRsi'],
            effective_rsi=ceiling['effectiveRsi'],
            area_metres=ceiling['area'],
            length_metres=ceiling['length']

        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'nominalRsi': self.nominal_rsi,
            'nominalR': (self.nominal_rsi * _RSI_MULTIPLIER) if self.nominal_rsi is not None else None,
            'effectiveRsi': self.effective_rsi,
            'effectiveR': (self.effective_rsi * _RSI_MULTIPLIER) if self.effective_rsi is not None else None,
            'areaMetres': self.area_metres,
            'areaFeet': (self.area_metres * _FEET_SQUARED_MULTIPLIER) if self.area_metres is not None else None,
            'lengthMetres': self.length_metres,
            'lengthFeet': (self.length_metres * _FEET_MULTIPLIER) if self.length_metres is not None else None
        }
