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


class _Window(typing.NamedTuple):
    label: typing.Optional[str]
    glazing_type_english: typing.Optional[str]
    glazing_type_french: typing.Optional[str]
    coatings_tints_english: typing.Optional[str]
    coatings_tints_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]
    rsi: typing.Optional[float]
    width: typing.Optional[float]
    height: typing.Optional[float]


class _WallCode(typing.NamedTuple):
    identifier: str
    label: typing.Optional[str]
    structure_type_english: typing.Optional[str]
    structure_type_french: typing.Optional[str]
    component_type_size_english: typing.Optional[str]
    component_type_size_french: typing.Optional[str]


class _WindowCode(typing.NamedTuple):
    identifier: str
    label: typing.Optional[str]
    glazing_type_english: typing.Optional[str]
    glazing_type_french: typing.Optional[str]
    coatings_tints_english: typing.Optional[str]
    coatings_tints_french: typing.Optional[str]
    fill_type_english: typing.Optional[str]
    fill_type_french: typing.Optional[str]
    spacer_type_english: typing.Optional[str]
    spacer_type_french: typing.Optional[str]
    type_english: typing.Optional[str]
    type_french: typing.Optional[str]
    frame_material_english: typing.Optional[str]
    frame_material_french: typing.Optional[str]


_RSI_MULTIPLIER = 5.678263337
_FEET_MULTIPLIER = 3.28084
_FEET_SQUARED_MULTIPLIER = _FEET_MULTIPLIER**2


class WallCode(_WallCode):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'type': 'string', 'required': True},
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'structureTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'structureTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'componentTypeSizeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'componentTypeSizeFrench': {'type': 'string', 'required': True, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls, wall_code: typing.Dict[str, typing.Optional[str]]) -> 'WallCode':
        return WallCode(
            identifier=wall_code['id'],
            label=wall_code['label'],
            structure_type_english=wall_code['structureTypeEnglish'],
            structure_type_french=wall_code['structureTypeFrench'],
            component_type_size_english=wall_code['componentTypeSizeEnglish'],
            component_type_size_french=wall_code['componentTypeSizeFrench'],
        )

class WindowCode(_WindowCode):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'id':  {'type': 'string', 'required': True},
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'glazingTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'glazingTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'coatingsTintsEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'coatingsTintsFrench': {'type': 'string', 'required': True, 'nullable': True},
                'fillTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'fillTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'spacerTypeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'spacerTypeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'typeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'typeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'frameMaterialEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'frameMaterialFrench': {'type': 'string', 'required': True, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls, wall_code: typing.Dict[str, typing.Optional[str]]) -> 'WindowCode':
        return WindowCode(
            identifier=wall_code['id'],
            label=wall_code['label'],
            glazing_type_english=wall_code['glazingTypeEnglish'],
            glazing_type_french=wall_code['glazingTypeFrench'],
            coatings_tints_english=wall_code['coatingsTintsEnglish'],
            coatings_tints_french=wall_code['coatingsTintsFrench'],
            fill_type_english=wall_code['fillTypeEnglish'],
            fill_type_french=wall_code['fillTypeFrench'],
            spacer_type_english=wall_code['spacerTypeEnglish'],
            spacer_type_french=wall_code['spacerTypeFrench'],
            type_english=wall_code['typeEnglish'],
            type_french=wall_code['typeFrench'],
            frame_material_english=wall_code['frameMaterialEnglish'],
            frame_material_french=wall_code['frameMaterialFrench'],
        )

class _Codes(typing.NamedTuple):
    wall: typing.Dict[str, WallCode]
    window: typing.Dict[str, WindowCode]


class Codes(_Codes):

    SCHEMA = {
        'type': 'dict',
        'required': True,
        'schema': {
            'wall': WallCode.SCHEMA,
            'window': WindowCode.SCHEMA,
        }
    }

    @classmethod
    def from_data(cls, codes: typing.Dict[str, typing.List[typing.Dict[str, str]]]):
        wall_code_list = (WallCode.from_data(wall_code) for wall_code in codes['wall'])
        window_code_list = (WindowCode.from_data(window_code) for window_code in codes['window'])

        wall_codes = {wall_code.identifier: wall_code for wall_code in wall_code_list}
        window_codes = {window_code.identifier: window_code for window_code in window_code_list}

        return Codes(
            wall=wall_codes,
            window=window_codes,
        )


class Wall(_Wall):

    SCHEMA = {
        'type': 'list',
        'required': True,
        'schema': {
            'type': 'dict',
            'schema': {
                'label':  {'type': 'string', 'required': True, 'nullable': True},
                'constructionTypeCode':  {'type': 'string', 'required': False, 'nullable': True},
                'constructionTypeNode':  {'type': 'string', 'required': False, 'nullable': True},
                'nominalRsi':  {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'effectiveRsi':  {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'perimeter':  {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'height':  {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
            }
        }
    }

    @classmethod
    def from_data(cls,
                  wall: typing.Dict[str, typing.Any],
                  wall_codes: typing.Dict[str, WallCode]):

        code_id = wall.get('constructionTypeCode')
        code = wall_codes.get(code_id)

        structure_type_english = code.structure_type_english if code is not None else None
        structure_type_french = code.structure_type_french if code is not None else None
        component_type_size_english = code.component_type_size_english if code is not None else None
        component_type_size_french = code.component_type_size_french if code is not None else None

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
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'typeEnglish': {'type': 'string', 'required': True, 'nullable': True},
                'typeFrench': {'type': 'string', 'required': True, 'nullable': True},
                'nominalRsi': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'effectiveRsi': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'area': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'length': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True}
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

    def to_dict(self):
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
                'label': {'type': 'string', 'required': True, 'nullable': True},
                'nominalRsi': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'effectiveRsi': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'area': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True},
                'length': {'type': 'float', 'required': True, 'coerce': float, 'nullable': True}
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

    def to_dict(self):
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
