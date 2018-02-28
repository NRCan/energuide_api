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

    _CODE_TAG_TRANSLATIONS = {
        code.WallCodeTag.STRUCTURE_TYPE: 'structureType',
        code.WallCodeTag.COMPONENT_TYPE_SIZE: 'componentTypeSize',
    }

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
        except (ElementGetValueError) as exc:
            raise InvalidEmbeddedDataTypeError(Wall) from exc

    @property
    def _wall_area(self) -> area.Area:
        return area.Area(self.perimeter.metres * self.height.metres)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        code_tags: typing.Dict[str, typing.Optional[str]] = dict(
            item
            for tag_name in self._CODE_TAG_TRANSLATIONS.values()
            for item in {
                f'{tag_name}English': None,
                f'{tag_name}French': None,
            }.items()
        )

        if self.wall_code:
            for tag_type, tag_name in self._CODE_TAG_TRANSLATIONS.items():
                tag_value = self.wall_code.tags.get(tag_type)
                code_tags.update(
                    **{
                        f'{tag_name}English': tag_value.english if tag_value else None,
                        f'{tag_name}French': tag_value.french if tag_value else None,
                    }
                )
        return {
            'label': self.label,
            **code_tags,
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
