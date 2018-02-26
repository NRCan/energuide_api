import typing
from energuide.embedded import area
from energuide.embedded import code
from energuide.embedded import insulation
from energuide.embedded import distance
from energuide import element
from energuide.exceptions import InvalidEmbeddedDataTypeError, ElementGetValueError


class _Wall(typing.NamedTuple):
    label: str
    wall_code: typing.Optional[code.WallCode]
    nominal_insulation: insulation.Insulation
    effective_insulation: insulation.Insulation
    perimeter: distance.Distance
    height: distance.Distance


class Wall(_Wall):

    @classmethod
    def from_data(cls,
                  wall: element.Element,
                  wall_codes: typing.Dict[str, code.WallCode]) -> 'Wall':

        code_id = wall.xpath('Construction/Type/@idref')
        wall_code = wall_codes[code_id[0]] if code_id else None

        try:
            return Wall(
                label=wall.get_text('Label'),
                wall_code=wall_code,
                nominal_insulation=insulation.Insulation(wall.get('Construction/Type/@nominalInsulation', float)),
                effective_insulation=insulation.Insulation(wall.get('Construction/Type/@rValue', float)),
                perimeter=distance.Distance(wall.get('Measurements/@perimeter', float)),
                height=distance.Distance(wall.get('Measurements/@height', float)),
            )
        except (ElementGetValueError, AssertionError) as exc:
            raise InvalidEmbeddedDataTypeError(Wall) from exc

    @property
    def _wall_area(self) -> area.Area:
        return area.Area(self.perimeter.metres * self.height.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            'label': self.label,
            'structureTypeEnglish': self.wall_code.structure_type.english if self.wall_code else None,
            'structureTypeFrench': self.wall_code.structure_type.french if self.wall_code else None,
            'componentTypeSizeEnglish': self.wall_code.component_type_size.english if self.wall_code else None,
            'componentTypeSizeFrench': self.wall_code.component_type_size.french if self.wall_code else None,
            'insulationNominalRsi': self.nominal_insulation.rsi,
            'insulationNominalR': self.nominal_insulation.r_value,
            'insulationEffectiveRsi': self.effective_insulation.rsi,
            'insulationEffectiveR': self.effective_insulation.r_value,
            'areaMetres': self._wall_area.square_metres,
            'areaFeet': self._wall_area.square_feet,
            'perimeterMetres': self.perimeter.metres,
            'perimeterFeet': self.perimeter.feet,
            'heightMetres': self.height.metres,
            'heightFeet': self.height.feet,
        }
